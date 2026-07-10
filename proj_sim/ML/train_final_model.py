import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# ===============================
# 1. LOAD DATA
# ===============================
df_sim = pd.read_csv(r"C:\Users\Raghuram S\Amrita\4th Sem\IoT\Project\proj_sim\Assets\sim_processed_data.csv")
df_real = pd.read_csv(r"C:\Users\Raghuram S\Amrita\4th Sem\IoT\Project\proj_sim\Assets\real_processed_data.csv")

print("Sim data:", df_sim.shape)
print("Real data:", df_real.shape)

# ===============================
# 2. MERGE DATASETS
# ===============================
df = pd.concat([df_sim, df_real], ignore_index=True)

print("\nCombined label distribution:")
print(df["label"].value_counts())

# ===============================
# 3. FEATURE SELECTION
# ===============================
FEATURES = [
    "gas_current",
    "gas_moving_avg",
    "gas_rate",
    "gas_variance",
    "acc_mag",
    "gyro_mag",
    "acc_var",
    "gyro_var"
]

X = df[FEATURES].values
y = df["label"].values
fall_flag = df["fall_flag"].values  # rule-based override

# ===============================
# 4. TRAIN / TEST SPLIT
# ===============================
X_train, X_test, y_train, y_test, fall_train, fall_test = train_test_split(
    X, y, fall_flag,
    test_size=0.25,
    shuffle=False
)


# ===============================
# 5. SCALING (ESP-friendly)
# ===============================
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ===============================
# 6. TRAIN LIGHTWEIGHT MODEL
# ===============================
model = LogisticRegression(
    multi_class="multinomial",
    class_weight="balanced",
    max_iter=500
)

model.fit(X_train, y_train)

# ===============================
# 7. PREDICTION WITH FALL OVERRIDE
# ===============================
y_pred = model.predict(X_test)

# Rule-based override
y_pred_final = []
for i in range(len(y_pred)):
    if fall_test[i] == 1:
        y_pred_final.append(2)   # Emergency
    else:
        y_pred_final.append(y_pred[i])

y_pred_final = np.array(y_pred_final)

# ===============================
# 8. EVALUATION
# ===============================
print("\nCONFUSION MATRIX:")
print(confusion_matrix(y_test, y_pred_final))

print("\nCLASSIFICATION REPORT:")
print(classification_report(y_test, y_pred_final))

# ===============================
# 9. SAVE MODEL PARAMETERS (ESP STEP NEXT)
# ===============================
np.save("model_weights.npy", model.coef_)
np.save("model_bias.npy", model.intercept_)
np.save("scaler_mean.npy", scaler.mean_)
np.save("scaler_scale.npy", scaler.scale_)

print("\nModel and scaler parameters saved for ESP deployment.")
