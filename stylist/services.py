import os
import tensorflow as tf
import cv2
import joblib
import numpy as np
from django.conf import settings


# def analyze_skin_tone(image_path):
#     model = tf.keras.models.load_model('stylist/ml_models/skin_tone_model.h5')
#     img = cv2.imread(image_path)
#     img = cv2.resize(img, (224, 224))
#     img = img / 255.0
#     img = np.expand_dims(img, axis=0)
#     mst_score = model.predict(img)[0][0]  # MST score (1-10)
#     return round(mst_score)

class FashionRecommender:
    def __init__(self):
        model_path = os.path.join(
            settings.BASE_DIR, 'stylist', 'ml_models', 'fashion_recommender.h5'
        )
        encoder_path = os.path.join(
            settings.BASE_DIR, 'stylist', 'ml_models', 'label_encoder.pkl'
        )

        self.model = tf.keras.models.load_model(model_path)
        self.encoder = joblib.load(encoder_path)

    def preprocess_image(self, image_path):
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        return img / 255.0
    
    def detect_skin_tone(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        lower_skin = np.array([0, 48, 80], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        skin = cv2.bitwise_and(image, image, mask=mask)
        skin_pixels = skin[np.where(mask != 0)]
        return np.mean(skin_pixels, axis=0) if len(skin_pixels) > 0 else None
    
    def classify_skin_tone(self, skin_mean):
        if skin_mean is None:
            return "Unknown"
        r, g, b = skin_mean
        if r > 200 and g > 150 and b > 100:
            return "Light"
        elif r > 150 and g > 100 and b > 80:
            return "Medium"
        else:
            return "Dark"
    
    def predict(self, image_path):
        try:
            # Preprocess image
            img = self.preprocess_image(image_path)
            if img is None:
                return None
            
            # Get skin tone
            skin_mean = self.detect_skin_tone(img)
            skin_tone = self.classify_skin_tone(skin_mean)
            
            # Predict colors
            img_array = np.expand_dims(img, axis=0)
            predictions = self.model.predict(img_array)
            predicted_class = np.argmax(predictions, axis=1)
            recommended_color = self.encoder.inverse_transform(predicted_class)[0]
            
            return {
                'skin_tone': skin_tone,
                'recommended_color': recommended_color,
                'confidence': float(np.max(predictions)),
                'color_options': list(self.encoder.classes_)
            }
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return None