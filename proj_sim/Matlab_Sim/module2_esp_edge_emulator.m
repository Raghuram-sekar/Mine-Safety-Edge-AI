clc; clear; close all;

%% ==============================
% MODULE 2: ESP EDGE AI + FAIL-SAFE
% ===============================

Fs = 1; T = 120;
t = 0:1:T; N = length(t);
window = 5;

%% ---------- SENSOR SIGNALS ----------
gas = 25 + 2*randn(1,N);
gas(t > 40 & t <= 60) = linspace(30,120,sum(t > 40 & t <= 60));
gas(t > 60) = 120 + 5*randn(1,sum(t > 60));

acc_mag = 1 + 0.05*randn(1,N);
acc_mag(t == 70) = 4.5;

gyro_mag = 20 + 2*randn(1,N);
gyro_mag(t == 70) = 120;

%% ---------- FAIL-SAFE EVENTS ----------
power_fail_t = 95;       % ESP power failure time
sensor_fail_t = 85;      % sensor stuck fault

%% ---------- PRETRAINED MODEL ----------
W = [ -15.95  -0.59  -0.46   0.36   0.09  -0.02  -0.01  -0.05;
        2.00   0.15  -0.09  -0.06   0.03  -0.01   0.04   0.03;
       13.95   0.44   0.55  -0.30  -0.12   0.02  -0.02   0.02 ];

b = [-24.9; 6.19; 18.7];
mu = [239.3 239.3 0 13727 2.95 44.2 1.90 423.5];
sigma = [124.0 66.4 164.4 10693 1.54 23.1 1.45 332.9];

%% ---------- BUFFERS ----------
gas_buf  = zeros(1,window);
acc_buf  = zeros(1,window);
gyro_buf = zeros(1,window);

%% ---------- THRESHOLDS ----------
ACC_THR  = 3.0;
GYRO_THR = 100;

%% ---------- FIGURE ----------
figure('Color','w','Position',[100 100 1200 650]); %[output:87d3981e]

subplot(2,2,1); title('Gas (ppm)'); grid on; xlim([0 T]); ylim([0 150]); %[output:87d3981e]
subplot(2,2,2); title('IMU Magnitudes'); grid on; xlim([0 T]); ylim([0 150]); %[output:87d3981e]
subplot(2,2,[3 4]); axis off; %[output:87d3981e]

sgtitle('Module 2: ESP Edge-AI with Fail-Safe Logic','FontWeight','bold'); %[output:87d3981e]

%% ---------- MAIN LOOP ----------
esp_alive = true;

for k = 1:N %[output:group:1148e686]

    % ---- POWER FAILURE ----
    if k == power_fail_t
        esp_alive = false;
    end

    % ---- ESP OFFLINE ----
    if ~esp_alive
        subplot(2,2,[3 4]); cla; axis off; %[output:51683f09]
        rectangle('Position',[0.15 0.3 0.7 0.4],'FaceColor',[0.3 0.3 0.3]);
        text(0.5,0.5,'ESP OFFLINE','Color','w',...
            'FontSize',22,'FontWeight','bold','HorizontalAlignment','center');
        drawnow;
        pause(0.05);
        continue;
    end

    % ---- SENSOR FAILURE (STUCK VALUE) ----
    if k >= sensor_fail_t
        gas(k) = gas(sensor_fail_t);
    end

    % Update buffers
    gas_buf  = [gas_buf(2:end),  gas(k)];
    acc_buf  = [acc_buf(2:end),  acc_mag(k)];
    gyro_buf = [gyro_buf(2:end), gyro_mag(k)];

    % Feature extraction
    gas_avg = mean(gas_buf);
    gas_var = var(gas_buf);
    gas_rate = gas(k) - gas(max(k-1,1));
    acc_var  = var(acc_buf);
    gyro_var = var(gyro_buf);

    % Sensor validity check
    sensor_invalid = (gas_var < 1e-3);

    % Feature vector
    x = [ gas(k), gas_avg, gas_rate, gas_var, ...
          acc_mag(k), gyro_mag(k), acc_var, gyro_var ];

    % ---- FAIL-SAFE PRIORITY ----
    if sensor_invalid
        status = "SENSOR FAULT";
        col = [0.5 0.5 0.5];
    else
        % Normalization
        x_hat = (x - mu) ./ sigma;

        % ML inference
        z = W * x_hat' + b;
        [~, cls] = max(z);

        % Fall override
        if acc_mag(k) > ACC_THR && gyro_mag(k) > GYRO_THR
            cls = 3;
        end

        switch cls
            case 1
                status = "NORMAL"; col = 'g';
            case 2
                status = "WARNING"; col = [0.9 0.6 0];
            case 3
                status = "EMERGENCY"; col = 'r';
        end
    end

    % Plots
    subplot(2,2,1); %[output:87d3981e]
    plot(t(1:k), gas(1:k),'LineWidth',2); grid on; %[output:87d3981e] %[output:51683f09]

    subplot(2,2,2);
    plot(t(1:k), acc_mag(1:k),'b',t(1:k),gyro_mag(1:k),'r','LineWidth',1.5); %[output:87d3981e] %[output:51683f09]
    legend('Acc','Gyro');

    % Status panel
    subplot(2,2,[3 4]); %[output:51683f09]
    cla; axis off;
    rectangle('Position',[0.2 0.3 0.6 0.4],'FaceColor',col,'Curvature',0.1);
    text(0.5,0.55,'ESP STATUS','HorizontalAlignment','center','FontSize',18,'Color','w');
    text(0.5,0.4,status,'HorizontalAlignment','center','FontSize',20,'Color','w','FontWeight','bold');

    drawnow;
    pause(0.05);
end %[output:group:1148e686]


%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"onright"}
%---
%[output:87d3981e]
%   data: {"dataType":"image","outputData":{"dataUri":"data:,","height":0,"width":0}}
%---
%[output:51683f09]
%   data: {"dataType":"image","outputData":{"dataUri":"data:,","height":0,"width":0}}
%---
