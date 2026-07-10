import numpy as np
import pandas as pd

# Time settings
T = 300
t = np.arange(0, T+1, 1)

# True gas concentration
gas_true = np.zeros_like(t, dtype=float)

for i in range(len(t)):
    if t[i] <= 100:
        gas_true[i] = 20
    elif t[i] <= 150:
        gas_true[i] = 20 + 0.6*(t[i]-100)
    else:
        gas_true[i] = 100 + 0.4*(t[i]-150)

# Save for MATLAB
data = pd.DataFrame({
    "time": t,
    "gas_true": gas_true
})

data.to_csv("mine_environment.csv", index=False)
print("Data saved to mine_environment.csv")