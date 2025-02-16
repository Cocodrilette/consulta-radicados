from django.urls import path, include

urlpatterns = [
    path('consulta_radicados/', include('api.consulta_radicados.urls')),
]
