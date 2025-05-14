from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import FashionRecommender
from .serializers import ImageUploadSerializer, AnalysisResultSerializer

class FashionAnalysisView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recommender = FashionRecommender()

    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data, context={'request': request, 'recommender': self.recommender})
        # Extract the image from the request
        if serializer.is_valid():
            analysis_result = serializer.save()
            result_serializer = AnalysisResultSerializer(analysis_result, context={'request': request})
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)