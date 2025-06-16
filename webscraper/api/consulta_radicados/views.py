from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import views


class ScrapeRadicados(views.APIView):
    def get(self):
        return Response({"message": "Scraping radicados..."})
