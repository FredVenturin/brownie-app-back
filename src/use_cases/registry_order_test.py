from unittest.mock import MagicMock
from datetime import datetime

from src.use_cases.registry_order import RegistryOrder
from src.main.http_types.http_request import HttpRequest


def test_registry_order_success():
    # cria mock do repositório
    mock_repository = MagicMock()

    controller = RegistryOrder(mock_repository)

    request = HttpRequest(
        body={
            "data": {
                "product": "Mouse",
                "quantity": 1
            }
        }
    )

    response = controller.registry(request)

    # status correto
    assert response.status_code == 201

    # banco foi chamado
    mock_repository.insert_document.assert_called_once()

    # verifica dados enviados
    args, _ = mock_repository.insert_document.call_args
    inserted_data = args[0]

    assert inserted_data["product"] == "Mouse"
    assert inserted_data["quantity"] == 1
    assert "created_at" in inserted_data


def test_registry_order_error():
    mock_repository = MagicMock()
    mock_repository.insert_document.side_effect = Exception("erro")

    controller = RegistryOrder(mock_repository)

    request = HttpRequest(
        body={"data": {"product": "Mouse"}}
    )

    response = controller.registry(request)

    assert response.status_code == 400