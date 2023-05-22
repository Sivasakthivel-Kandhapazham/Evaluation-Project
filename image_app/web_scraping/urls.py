from django.urls import path
from . import views


urlpatterns = [
    path('web_scraping', views.web_scraping_view, name = "web_scraping")
]