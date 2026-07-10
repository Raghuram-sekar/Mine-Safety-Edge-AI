clc; clear; close all;

%% ==============================
% MODULE 3: PACKET-LEVEL LoRa SIM
% ===============================

Fs = 1; T = 120;
t = 0:1:T; N = length(t);

%% ---------- SYSTEM PARAMETERS ----------
NODE_ID = 1;

packet_loss_prob = 0.2;      % 20% packet loss
lora_delay_mean = 2;         % seconds
lora_delay_jitter = 1;       % seconds

gateway_log = {};

%% ---------- ESP DECISION (FROM MODULE 2) ----------
% Predefined decision timeline for demo
decision = strings(1,N);
decision(:) = "NORMAL";
decision(45:60) = "WARNING";
decision(61:90) = "EMERGENCY";
decision(95:end) = "OFFLINE";

%% ---------- FIGURE ----------
figure('Color','w','Position',[100 100 1200 500]); %[output:843b28a0]

subplot(1,2,1); %[output:843b28a0]
hESP = text(0.5,0.5,'','FontSize',18,'HorizontalAlignment','center'); %[output:843b28a0]
axis off; %[output:843b28a0]
title('ESP Node'); %[output:843b28a0]

subplot(1,2,2); %[output:843b28a0]
hGW = text(0.5,0.5,'','FontSize',18,'HorizontalAlignment','center'); %[output:843b28a0]
axis off; %[output:843b28a0]
title('Gateway'); %[output:843b28a0]

sgtitle('Module 3: Packet-Level LoRa Communication','FontWeight','bold'); %[output:843b28a0]

%% ---------- MAIN LOOP ----------
for k = 1:N %[output:group:131ed219]

    % ESP STATUS DISPLAY
    subplot(1,2,1); cla; axis off; %[output:843b28a0]
    text(0.5,0.6,"ESP STATUS",'HorizontalAlignment','center','FontSize',16);
    text(0.5,0.45,decision(k),'HorizontalAlignment','center','FontSize',20);

    % Decide if packet is sent
    send_packet = (decision(k) == "EMERGENCY" || decision(k) == "OFFLINE");

    if send_packet && decision(k) ~= "OFFLINE"

        % Create packet
        packet.node = NODE_ID;
        packet.time = k;
        packet.status = decision(k);

        % Channel loss
        if rand < packet_loss_prob
            packet_received = false;
        else
            packet_received = true;
            delay = max(0, lora_delay_mean + randn*lora_delay_jitter);
        end

        % Gateway processing
        subplot(1,2,2); cla; axis off; %[output:843b28a0]

        if packet_received
            pause(delay);
            gateway_log{end+1} = packet;
            text(0.5,0.6,"PACKET RECEIVED",'Color','g',...
                'HorizontalAlignment','center','FontSize',16);
            text(0.5,0.45,"Status: " + packet.status,...
                'HorizontalAlignment','center','FontSize',18);
        else
            text(0.5,0.6,"PACKET LOST",'Color','r',...
                'HorizontalAlignment','center','FontSize',16);
        end

    elseif decision(k) == "OFFLINE"
        subplot(1,2,2); cla; axis off; %[output:843b28a0]
        text(0.5,0.5,"NODE OFFLINE",'Color',[0.5 0.5 0.5],...
            'HorizontalAlignment','center','FontSize',20);
    end

    drawnow;
    pause(0.2);
end %[output:group:131ed219]

%% ---------- GATEWAY LOG ----------
disp("Gateway Event Log:"); %[output:7d5e3255]
disp(gateway_log); %[output:8a1104d2]


%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"onright"}
%---
%[output:843b28a0]
%   data: {"dataType":"image","outputData":{"dataUri":"data:,","height":0,"width":0}}
%---
%[output:7d5e3255]
%   data: {"dataType":"text","outputData":{"text":"Gateway Event Log:\n","truncated":false}}
%---
%[output:8a1104d2]
%   data: {"dataType":"text","outputData":{"text":"    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}    {1×1 struct}\n\n","truncated":false}}
%---
