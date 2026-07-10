import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
df_raw = pd.read_csv(r"C:\Users\aadih\Desktop\desktop\work\semester 4\IOT and Communication\proj\Dataset\mine_safety_dataset_v2.csv")

# Acceleration magnitude
df_raw["acc_mag"] = np.sqrt(
    df_raw["ax"]**2 +
    df_raw["ay"]**2 +
    df_raw["az"]**2
)

# Gyroscope magnitude
df_raw["gyro_mag"] = np.sqrt(
    df_raw["gx"]**2 +
    df_raw["gy"]**2 +
    df_raw["gz"]**2
)

# Sliding window (ESP-realistic)
window = 5

df_raw["acc_var"] = df_raw["acc_mag"].rolling(window).var()
df_raw["gyro_var"] = df_raw["gyro_mag"].rolling(window).var()

# Drop NaNs from rolling window
df_imu = df_raw.dropna().reset_index(drop=True)

print(df_imu[["acc_mag", "gyro_mag", "acc_var", "gyro_var"]].head())
plt.figure(figsize=(10,4))
plt.plot(df_imu["acc_mag"], label="Acceleration Magnitude")
plt.xlabel("Samples")
plt.ylabel("Magnitude")
plt.title("Acceleration Magnitude Over Time")
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(10,4))
plt.plot(df_imu["gyro_mag"], label="Gyro Magnitude", color="orange")
plt.xlabel("Samples")
plt.ylabel("Magnitude")
plt.title("Gyroscope Magnitude Over Time")
plt.legend()
plt.grid()
plt.show()

# Thresholds (derived from dataset statistics)
acc_spike_thresh = df_imu["acc_mag"].mean() + 3*df_imu["acc_mag"].std()
gyro_spike_thresh = df_imu["gyro_mag"].mean() + 3*df_imu["gyro_mag"].std()

df_imu["fall_flag"] = (
    (df_imu["acc_mag"] > acc_spike_thresh) &
    (df_imu["gyro_mag"] > gyro_spike_thresh)
).astype(int)

print(df_imu["fall_flag"].value_counts())
# -------- GAS FEATURES --------
window = 5

df_imu["gas_current"] = df_imu["gas"]
df_imu["gas_moving_avg"] = df_imu["gas"].rolling(window).mean()
df_imu["gas_rate"] = df_imu["gas"].diff()
df_imu["gas_variance"] = df_imu["gas"].rolling(window).var()

df_imu = df_imu.dropna().reset_index(drop=True)

def assign_final_label(row):
    if row["fall_flag"] == 1 or row["gas_current"] >= 100:
        return 2   # Emergency
    elif row["gas_current"] >= 30:
        return 1   # Warning
    else:
        return 0   # Normal

df_imu["label"] = df_imu.apply(assign_final_label, axis=1)

print(df_imu["label"].value_counts())

df_imu.to_csv("real_processed_data.csv", index=False)
print("Processed data saved to real_processed_data.csv")
