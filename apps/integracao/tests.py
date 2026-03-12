import pytest


@pytest.mark.django_db
class TestMelhorEnvioIntegration:
    def test_calculate_shipping_cost(self, api_client):
        payload = {
            "to": {
                "postal_code": "58483000",
            },
            "package": {
                "height": 10,
                "width": 15,
                "length": 20,
                "weight": 1.0,
            }
        }

        response = api_client.post("/api/integracao/melhorenvio/frete/", payload, format="json")

        assert response.status_code == 200
        assert len(response.data) == 2
        option1 = response.data[0]
        assert "company" in option1
        assert "name" in option1
        option2 = response.data[1]
        assert "company" in option2
        assert "name" in option2
