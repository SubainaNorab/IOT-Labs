import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Step 1: Generate Synthetic Data
np.random.seed(42)
data_size = 300
temperature = np.random.uniform(15, 35, size=data_size)  # in Celsius
humidity = np.random.uniform(30, 90, size=data_size)     # in Percent

# Step 2: Label Assignment
labels = []
for t, h in zip(temperature, humidity):
    if t < 20 or h < 40:
        labels.append("Cold")
    elif 20 <= t <= 28 and 40 <= h <= 70:
        labels.append("Comfort")
    else:
        labels.append("Hot")

# Step 3: Save Dataset to CSV (Optional)
df = pd.DataFrame({
    "temperature": temperature,
    "humidity": humidity,
    "comfort_level": labels
})
df.to_csv("dht11_data.csv", index=False)

# Step 4: Encode Labels
label_encoder = LabelEncoder()
df["label_encoded"] = label_encoder.fit_transform(df["comfort_level"])

# Step 5: Feature Scaling
X = df[["temperature", "humidity"]].values
y = tf.keras.utils.to_categorical(df["label_encoded"].values, num_classes=3)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 6: Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 7: Build Model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=(2,)),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Step 8: Train Model
model.fit(X_train, y_train, validation_split=0.2, epochs=50, verbose=1)

# Step 9: Evaluate & Save
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print(f"\nTest Accuracy: {acc:.2f}")

model.save("model.h5")
print("Saved model.h5")

# Step 10: Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open("model.tflite", "wb") as f:
    f.write(tflite_model)

print("Saved model.tflite")
