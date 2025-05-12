from django.contrib import admin
from django.urls import path
from users.views import UserProfileView
from stylist.views import SkinToneAnalysisView
from retail.views import ProductAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', UserProfileView.as_view()),
    path('api/skin-tone/', SkinToneAnalysisView.as_view()),
    path('api/products/', ProductAPIView.as_view()),
]
