#!/usr/bin/env python3
"""
Edge-ML LoRa simulation (SimPy)
Nodes run TinyML locally and send alert packets only.
Outputs: avg alert latency, PDR, channel utilization, collisions across node counts.
"""

import simpy
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import math
import statistics
import time

# -------------------- CONFIG --------------------
RANDOM_SEED = 42
SIM_DURATION = 600.0         # seconds per run
EVENT_RATE_PER_MIN = 0.5     # avg events per minute per node (Poisson)
EVENT_RATE = EVENT_RATE_PER_MIN / 60.0
T_ALERT_PAYLOAD_BYTES = 32
SF_DEFAULT = 9
BW = 125e3
CR = 1
MAX_RETRIES = 2
DUTY_CYCLE = 0.01            # 1% simple cooldown model
TPR = 0.95                   # node model true positive rate
FPR = 0.01                   # false positive rate
NODE_COUNTS = [10, 20, 50, 100]
RUNS_PER_SCENARIO = 5

# -------------------- HELPERS --------------------
def lora_time_on_air(payload_bytes, sf=SF_DEFAULT, bw=BW, cr=CR, preamble=8):
    """
    Simple LoRa Time-on-Air approximation (seconds)
    Not full Semtech detail but consistent for comparisons.
    """
    ts = (2.0**sf) / bw
    payload_symb = 8 + max(math.ceil((8*payload_bytes - 4*sf + 28 + 16 - 20) / (4*(sf - 2))) * (cr + 4), 0)
    total_symb = preamble + 4.25 + payload_symb
    toa = total_symb * ts
    return float(toa)

TOA_ALERT = lora_time_on_air(T_ALERT_PAYLOAD_BYTES, sf=SF_DEFAULT)

# -------------------- CHANNEL & NODE --------------------
class Channel:
    def __init__(self, env):
        self.env = env
        self.active = []   # (node_id, end_time, pkt_ref)
        self.collisions = 0
        self.busy_time = 0.0
        self.last_busy_change = env.now
        self.busy = False

    def start_tx(self, node_id, duration, pkt_ref, guard=0.0):
        now = self.env.now
        collided = False
        for (_, end_t, _) in self.active:
            if end_t > now - guard:
                collided = True
                break
        end_time = now + duration
        self.active.append((node_id, end_time, pkt_ref))
        if collided:
            pkt_ref['success'] = False
            # Mark overlapping active as failed too
            for i, (n, end_t, p) in enumerate(self.active):
                if p is not pkt_ref and end_t > now - guard:
                    p['success'] = False
            self.collisions += 1
        else:
            pkt_ref['success'] = True
        if not self.busy:
            self.busy = True
            self.last_busy_change = now
        return end_time

    def finish_tx(self, pkt_ref):
        now = self.env.now
        self.active = [a for a in self.active if a[2] is not pkt_ref]
        if not self.active and self.busy:
            self.busy = False
            self.busy_time += now - self.last_busy_change

    def get_busy_fraction(self, sim_duration):
        if self.busy:
            self.busy_time += self.env.now - self.last_busy_change
            self.busy = False
        return self.busy_time / sim_duration if sim_duration > 0 else 0.0

class Node:
    def __init__(self, env, node_id, channel, event_rate, t_alert, tpr, fpr, duty_cycle, max_retries):
        self.env = env
        self.id = node_id
        self.channel = channel
        self.event_rate = event_rate
        self.t_alert = t_alert
        self.tpr = tpr
        self.fpr = fpr
        self.duty_cycle = duty_cycle
        self.max_retries = max_retries
        self.next_available_time = 0.0
        self.sent_alerts = 0
        self.successful_alerts = 0
        self.latencies = []
        self.collisions = 0
        self.proc = env.process(self.run())

    def run(self):
        while True:
            wait = random.expovariate(self.event_rate) if self.event_rate > 0 else float('inf')
            yield self.env.timeout(wait)
            event_time = self.env.now
            detected = random.random() < self.tpr
            if detected:
                if self.env.now < self.next_available_time:
                    yield self.env.timeout(self.next_available_time - self.env.now)
                attempt = 0
                sent_ok = False
                while attempt <= self.max_retries and not sent_ok:
                    attempt += 1
                    pkt = {'success': True, 'start': self.env.now}
                    end = self.channel.start_tx(self.id, self.t_alert, pkt)
                    yield self.env.timeout(self.t_alert)
                    self.channel.finish_tx(pkt)
                    self.sent_alerts += 1
                    if pkt['success']:
                        self.successful_alerts += 1
                        self.latencies.append(self.env.now - event_time)
                        sent_ok = True
                    else:
                        self.collisions += 1
                        backoff = random.uniform(0.05, 0.2)
                        yield self.env.timeout(backoff)
                cooldown = max(self.t_alert / self.duty_cycle - self.t_alert, 0.0)
                self.next_available_time = self.env.now + cooldown
            # false positive chance
            if random.random() < self.fpr:
                if self.env.now < self.next_available_time:
                    yield self.env.timeout(self.next_available_time - self.env.now)
                attempt = 0
                sent_ok = False
                fp_time = self.env.now
                while attempt <= self.max_retries and not sent_ok:
                    attempt += 1
                    pkt = {'success': True, 'start': self.env.now}
                    end = self.channel.start_tx(self.id, self.t_alert, pkt)
                    yield self.env.timeout(self.t_alert)
                    self.channel.finish_tx(pkt)
                    self.sent_alerts += 1
                    if pkt['success']:
                        self.successful_alerts += 1
                        self.latencies.append(self.env.now - fp_time)
                        sent_ok = True
                    else:
                        self.collisions += 1
                        backoff = random.uniform(0.05, 0.2)
                        yield self.env.timeout(backoff)
                cooldown = max(self.t_alert / self.duty_cycle - self.t_alert, 0.0)
                self.next_available_time = self.env.now + cooldown

# -------------------- RUNNER --------------------
def run_simulation(num_nodes=10, sim_duration=SIM_DURATION, seed=None):
    random.seed(seed)
    np.random.seed(seed if seed is not None else 0)
    env = simpy.Environment()
    channel = Channel(env)
    nodes = [Node(env, i, channel, EVENT_RATE, TOA_ALERT, TPR, FPR, DUTY_CYCLE, MAX_RETRIES) for i in range(num_nodes)]
    env.run(until=sim_duration)
    total_sent = sum(n.sent_alerts for n in nodes)
    total_success = sum(n.successful_alerts for n in nodes)
    all_lat = [lat for n in nodes for lat in n.latencies]
    avg_lat = statistics.mean(all_lat) if all_lat else None
    pdr = total_success / total_sent if total_sent > 0 else None
    busy = channel.get_busy_fraction(sim_duration)
    collisions = channel.collisions
    return {'num_nodes': num_nodes, 'total_sent': total_sent, 'total_success': total_success,
            'avg_latency': avg_lat, 'pdr': pdr, 'channel_busy': busy, 'collisions': collisions,
            'all_latencies': all_lat}

def batch_experiments(node_counts=NODE_COUNTS, runs=RUNS_PER_SCENARIO):
    results = []
    for n in node_counts:
        for run in range(runs):
            seed = RANDOM_SEED + n*run + run*97
            res = run_simulation(num_nodes=n, sim_duration=SIM_DURATION, seed=seed)
            res['run'] = run
            results.append(res)
            print(f"nodes={n} run={run} sent={res['total_sent']} succ={res['total_success']} pdr={res['pdr']}")
    return pd.DataFrame(results)

# -------------------- MAIN --------------------
if __name__ == "__main__":
    start = time.time()
    df = batch_experiments()
    print("Total time:", time.time() - start)
    # plotting
    grouped = df.groupby('num_nodes')
    mean_pdr = grouped['pdr'].mean()
    mean_lat = grouped['avg_latency'].apply(lambda x: np.nanmean([v for v in x if v is not None]))
    mean_busy = grouped['channel_busy'].mean()
    mean_coll = grouped['collisions'].mean()

    fig, axs = plt.subplots(2,2, figsize=(12,9))
    axs[0,0].plot(mean_pdr.index, mean_pdr.values, marker='o'); axs[0,0].set_title('Mean PDR vs # nodes'); axs[0,0].set_ylabel('PDR')
    axs[0,1].plot(mean_lat.index, mean_lat.values, marker='o'); axs[0,1].set_title('Mean Latency (s) vs # nodes'); axs[0,1].set_ylabel('Latency (s)')
    axs[1,0].plot(mean_busy.index, mean_busy.values, marker='o'); axs[1,0].set_title('Channel Utilization vs # nodes'); axs[1,0].set_ylabel('Busy fraction')
    axs[1,1].plot(mean_coll.index, mean_coll.values, marker='o'); axs[1,1].set_title('Collisions vs # nodes'); axs[1,1].set_ylabel('Collisions')
    for ax in axs.flat:
        ax.set_xlabel('# nodes')
    plt.tight_layout()
    plt.show()

    # histogram for largest node count
    max_n = max(NODE_COUNTS)
    sample = df[df['num_nodes']==max_n]['all_latencies'].values
    flat = [x for arr in sample for x in (arr if arr is not None else [])]
    plt.figure(figsize=(8,4))
    plt.hist(flat, bins=30)
    plt.title(f"Latency distribution for N={max_n}")
    plt.xlabel("Latency (s)"); plt.ylabel("count")
    plt.show()

    df.to_csv('edge_ml_sim_results.csv', index=False)
    print("Saved edge_ml_sim_results.csv")
