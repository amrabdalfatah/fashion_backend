from rest_framework.views import APIView
from rest_framework.response import Response
from .services import analyze_skin_tone

class SkinToneAnalysisView(APIView):
    def post(self, request):
        image = request.FILES['image']
        tone = analyze_skin_tone(image.temporary_file_path())
        return Response({"skin_tone": tone})