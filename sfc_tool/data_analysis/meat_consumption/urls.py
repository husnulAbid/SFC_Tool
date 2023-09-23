from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from . import views

app_name = "meat_consumption"

urlpatterns = [
    path("api_1/get_all_type_countrywise/", views.TotatConsumptionOverTime.as_view()),
    path("api_1/available_countries/", views.AvailableCountries.as_view()),
    path("api_1/start_and_end_year/", views.StartAndEndYear.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
