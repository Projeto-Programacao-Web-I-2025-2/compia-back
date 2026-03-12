from rest_framework import serializers


class MelhorEnvioFromToSerializer(serializers.Serializer):
    postal_code = serializers.CharField(help_text="CEP destino. Exemplo: 58483000")


class MelhorEnvioPackageSerializer(serializers.Serializer):
    height = serializers.FloatField(help_text="Altura em cm")
    width = serializers.FloatField(help_text="Largura em cm")
    length = serializers.FloatField(help_text="Comprimento em cm")
    weight = serializers.FloatField(help_text="Peso em kg")


class MelhorEnvioFreteSerializer(serializers.Serializer):
    to = MelhorEnvioFromToSerializer(write_only=True, required=True)
    package = MelhorEnvioPackageSerializer(write_only=True, required=True)

    class Meta:
        ref_name = "MelhorEnvioFrete"
