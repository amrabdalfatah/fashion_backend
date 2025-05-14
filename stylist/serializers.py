from rest_framework import serializers

from .models import OutfitRecommendation, AnalysisResult

class AnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = ['id', 'user', 'image_path', 'skin_tone', 'recommended_color', 'confidence', 'color_options', 'created_at']


class OutfitRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutfitRecommendation
        fields = ['id', 'user', 'occasion', 'generated_at', 'products']

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)

    def create(self, validate_data):
        recommender = self.context.get('recommender')
        image = validate_data['image']
        analysis_result = AnalysisResult(image_path=image.path)
        analysis_result.save()

        image_path = analysis_result.image_path

        prediction = recommender.predict(image_path) 

        if prediction:
            analysis_result.skin_tone = prediction['skin_tone']
            analysis_result.recommended_color = prediction['recommended_color']
            analysis_result.confidence = prediction['confidence']
            analysis_result.color_options = prediction['color_options']
            analysis_result.save()

        
        # Custom validation logic can be added here
        return analysis_result