import numpy as np

W = np.load("model_weights.npy")
b = np.load("model_bias.npy")
mean = np.load("scaler_mean.npy")
scale = np.load("scaler_scale.npy")

print("Weights:\n", W)
print("Bias:\n", b)
print("Scaler mean:\n", mean)
print("Scaler scale:\n", scale)
