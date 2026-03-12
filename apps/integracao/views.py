import requests
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from compia.settings import MELHOR_ENVIO_TOKEN, MELHOR_ENVIO_URL, EMAIL_HOST_USER
from .serializers import MelhorEnvioFreteSerializer


class MelhorEnvioFreteView(APIView):
    @extend_schema(
        request=MelhorEnvioFreteSerializer,
        summary="Consulta frete no MelhorEnvio",
    )
    def post(self, request):
        serializer = MelhorEnvioFreteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        payload = {
            "from": data["from"],
            "to": data["to"],
            "products": [
                {
                    "width": data["package"]["width"],
                    "height": data["package"]["height"],
                    "length": data["package"]["length"],
                    "weight": data["package"]["weight"],
                }
            ],
        }

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {MELHOR_ENVIO_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": f"Aplicação {EMAIL_HOST_USER}",
        }

        try:
            response = requests.post(MELHOR_ENVIO_URL, json=payload, headers=headers)
            response.raise_for_status()
            options = response.json()
            return Response(options[:2])
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
