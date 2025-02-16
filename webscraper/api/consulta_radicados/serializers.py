from rest_framework import serializers

class RadicadoSerializer(serializers.Serializer):
    fecha = serializers.CharField(max_length=100)
    despacho = serializers.CharField(max_length=100)
    sujeto = serializers.CharField(max_length=100)