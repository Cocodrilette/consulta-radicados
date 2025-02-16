from django.urls import path
from api.consulta_radicados import views

urlpatterns = [
    path('scrape/', views.ScrapeRadicados.as_view()),
]