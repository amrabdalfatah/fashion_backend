from django.contrib import admin
from django.urls import path
from users.views import UserProfileView
from stylist.views import FashionAnalysisView
from retail.views import ProductAPIView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', UserProfileView.as_view()),
    path('api/analyze/', FashionAnalysisView.as_view()),
    path('api/products/', ProductAPIView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
