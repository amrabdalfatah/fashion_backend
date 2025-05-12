import tensorflow as tf
import cv2
import numpy as np

def analyze_skin_tone(image_path):
    model = tf.keras.models.load_model('stylist/ml_models/skin_tone_model.h5')
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    mst_score = model.predict(img)[0][0]  # MST score (1-10)
    return round(mst_score)