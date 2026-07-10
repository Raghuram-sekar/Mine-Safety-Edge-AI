#include <Arduino.h>
#include <math.h>

#define NUM_FEATURES 8
#define NUM_CLASSES 3

#define GAS_PIN 34   // Example ADC pin
#define LED_PIN 2    // Built-in LED

const float weights[NUM_CLASSES][NUM_FEATURES] = {
  {-15.9546, -0.5905, -0.4588,  0.3590,  0.0908, -0.0179, -0.0129, -0.0466},
  {  2.0058,  0.1471, -0.0888, -0.0627,  0.0325, -0.0068,  0.0366,  0.0299},
  { 13.9487,  0.4434,  0.5476, -0.2962, -0.1233,  0.0247, -0.0237,  0.0167}
};

const float bias[NUM_CLASSES] = {
  -24.8972,
    6.1943,
   18.7030
};

const float scaler_mean[NUM_FEATURES] = {
  239.3555, 239.3222, -0.0321, 13727.6814,
    2.9546,  44.2766,  1.9015,  423.5437
};

const float scaler_scale[NUM_FEATURES] = {
  124.0559,  66.4830, 164.4597, 10693.6579,
    1.5490,  23.1045,   1.4524,   332.9319
};
float normalize(float x, float mean, float scale) {
    return (x - mean) / scale;
}
int ml_predict(float features[NUM_FEATURES]) {
    float z[NUM_CLASSES] = {0};

    for (int k = 0; k < NUM_CLASSES; k++) {
        z[k] = bias[k];
        for (int i = 0; i < NUM_FEATURES; i++) {
            float x = normalize(features[i], scaler_mean[i], scaler_scale[i]);
            z[k] += weights[k][i] * x;
        }
    }

    int cls = 0;
    float maxv = z[0];
    for (int k = 1; k < NUM_CLASSES; k++) {
        if (z[k] > maxv) {
            maxv = z[k];
            cls = k;
        }
    }
    return cls; // 0=Normal, 1=Warning, 2=Emergency
}
float readGas() {
    return 120.0; // fake ppm (change this to test)
}

void readIMU(float *ax, float *ay, float *az,
             float *gx, float *gy, float *gz) {
    *ax = 0.2;
    *ay = 0.1;
    *az = 1.0;
    *gx = 10.0;
    *gy = 5.0;
    *gz = 3.0;
}
void computeFeatures(float features[NUM_FEATURES]) {
    float ax, ay, az, gx, gy, gz;
    readIMU(&ax, &ay, &az, &gx, &gy, &gz);

    float gas = readGas();

    float acc_mag = sqrt(ax*ax + ay*ay + az*az);
    float gyro_mag = sqrt(gx*gx + gy*gy + gz*gz);

    features[0] = gas;
    features[1] = gas;   // placeholder avg
    features[2] = 0.0;   // placeholder rate
    features[3] = 0.0;   // placeholder variance
    features[4] = acc_mag;
    features[5] = gyro_mag;
    features[6] = 0.0;
    features[7] = 0.0;
}
void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
}

void loop() {
    float features[NUM_FEATURES];
    computeFeatures(features);

    int decision = ml_predict(features);

    Serial.print("Decision: ");
    Serial.println(decision);

    if (decision == 2) {
        digitalWrite(LED_PIN, HIGH);
    } else {
        digitalWrite(LED_PIN, LOW);
    }

    delay(1000);
}

