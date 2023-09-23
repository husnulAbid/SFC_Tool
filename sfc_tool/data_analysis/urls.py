from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from . import views

app_name = "data_analysis"

urlpatterns = [
    path('meat_consumption/', include("data_analysis.meat_consumption.urls"),),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
