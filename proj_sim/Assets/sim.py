import numpy as np
import scipy.io as sio
import pandas as pd

# Load MATLAB sensor data
mat = sio.loadmat(r"C:\Users\aadih\Desktop\desktop\work\semester 4\IOT and Communication\proj_sim\sensor_output.mat")


t = mat["t"].flatten()
sensor = mat["sensor_output_1"].flatten()

# Feature parameters
window = 5  # seconds

features = []

for i in range(len(sensor)):
    if i < window:
        continue

    current = sensor[i]
    moving_avg = np.mean(sensor[i-window:i])
    rate_of_change = sensor[i] - sensor[i-1]
    variance = np.var(sensor[i-window:i])

    features.append([t[i], current, moving_avg, rate_of_change, variance])

# Convert to DataFrame
df = pd.DataFrame(
    features,
    columns=["time", "current", "moving_avg", "rate_of_change", "variance"]
)
df = df.rename(columns={
    "current": "gas_current",
    "moving_avg": "gas_moving_avg",
    "rate_of_change": "gas_rate",
    "variance": "gas_variance"
})

print(df.head())

# Label generation based on safety standards
labels = []

for avg in df["gas_moving_avg"]:
    if avg < 30:
        labels.append(0)      # Normal
    elif avg < 100:
        labels.append(1)      # Warning
    else:
        labels.append(2)      # Emergency

df["label"] = labels

print(df.head())
print(df["label"].value_counts())

df["acc_mag"] = 0
df["gyro_mag"] = 0
df["acc_var"] = 0
df["gyro_var"] = 0
df["fall_flag"] = 0
df.to_csv("sim_processed_data.csv", index=False)
