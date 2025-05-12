import requests
from rest_framework.views import APIView
from rest_framework.response import Response

class ProductAPIView(APIView):
    def get(self, request):
        response = requests.get('https://api.shopify.com/products')
        return Response(response.json())