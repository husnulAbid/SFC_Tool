from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from . import views

app_name = "career_track"

urlpatterns = [
    path("api_1/view/", views.CareerTrackView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
