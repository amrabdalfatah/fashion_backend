import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
import os

# Load labels
labels_df = pd.read_csv('ml_models/labels.csv')

# Filter valid images (optional)
valid_images = [f for f in os.listdir('ml_models/images') if f.endswith('.jpg')]
labels_df = labels_df[labels_df['image_id'].isin(valid_images)]

# Map MST labels (1-10) to binary/multi-class
labels_df['label'] = labels_df['mst_score']  # Use 10 classes

train_df, test_df = train_test_split(labels_df, test_size=0.2, random_state=42)
train_df, val_df = train_test_split(train_df, test_size=0.1, random_state=42)

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)

# Validation/Test: Only rescale
val_datagen = ImageDataGenerator(rescale=1./255)

# Create generators
train_generator = train_datagen.flow_from_dataframe(
    dataframe=train_df,
    directory='mst_dataset/images',
    x_col='image_id',
    y_col='label',
    target_size=(224, 224),
    batch_size=32,
    class_mode='raw'  # For regression (MST 1-10)
)

val_generator = val_datagen.flow_from_dataframe(
    dataframe=val_df,
    directory='mst_dataset/images',
    x_col='image_id',
    y_col='label',
    target_size=(224, 224),
    batch_size=32,
    class_mode='raw'
)

# Load MobileNetV2 (exclude top layer)
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze base layers
base_model.trainable = False

# Add custom head
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
predictions = Dense(1, activation='linear')(x)  # Regression (MST 1-10)

model = Model(inputs=base_model.input, outputs=predictions)


model.compile(
    optimizer='adam',
    loss='mse',  # Mean Squared Error for regression
    metrics=['mae']  # Mean Absolute Error
)

history = model.fit(
    train_generator,
    epochs=10,
    validation_data=val_generator
)

test_generator = val_datagen.flow_from_dataframe(
    dataframe=test_df,
    directory='mst_dataset/images',
    x_col='image_id',
    y_col='label',
    target_size=(224, 224),
    batch_size=32,
    class_mode='raw'
)

loss, mae = model.evaluate(test_generator)
print(f"Test MAE: {mae:.2f} (Close to 0 is better)")

# Save the model
model.save('skin_tone_model.h5')
print("Model saved to stylist/ml_models/skin_tone_model.h5")