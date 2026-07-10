def fuse_decisions(imu_pred, gas_label):

    # Emergency conditions
    if imu_pred == 1:
        return 2   # Fall detected

    if gas_label == 2:
        return 2   # Gas emergency

    # Warning condition
    if gas_label == 1:
        return 1

    # Otherwise safe
    return 0

