import pytest
from unittest.mock import MagicMock
from bson.objectid import ObjectId

from src.models.repository.orders_repository import OrdersRepository


@pytest.fixture
def mock_repository():
    mock_db = MagicMock()
    mock_collection = MagicMock()

    mock_db.get_collection.return_value = mock_collection

    repository = OrdersRepository(mock_db)

    return repository, mock_collection


def test_insert_document(mock_repository):
    repository, mock_collection = mock_repository

    document = {"name": "Fred"}
    repository.insert_document(document)

    mock_collection.insert_one.assert_called_once_with(document)


def test_insert_list_of_documents(mock_repository):
    repository, mock_collection = mock_repository

    documents = [{"name": "A"}, {"name": "B"}]
    repository.insert_list_of_documents(documents)

    mock_collection.insert_many.assert_called_once_with(documents)


def test_select_one(mock_repository):
    repository, mock_collection = mock_repository

    doc_filter = {"name": "Fred"}
    repository.select_one(doc_filter)

    mock_collection.find_one.assert_called_once_with(doc_filter)


def test_select_many(mock_repository):
    repository, mock_collection = mock_repository

    doc_filter = {"status": "active"}
    repository.select_many(doc_filter)

    mock_collection.find.assert_called_once_with(doc_filter)


def test_select_many_with_properties(mock_repository):
    repository, mock_collection = mock_repository

    doc_filter = {"status": "active"}
    repository.select_many_with_properties(doc_filter)

    mock_collection.find.assert_called_once_with(
        doc_filter,
        {"_id": 0, "cupom": 0}
    )


def test_select_if_property_exists(mock_repository):
    repository, mock_collection = mock_repository

    repository.select_if_property_exists()

    mock_collection.find_one.assert_called_once_with(
        {"address": {"$exists": True}},
        {"_id": 0, "cupom": 0}
    )


def test_select_by_object_id(mock_repository):
    repository, mock_collection = mock_repository

    test_id = "507f1f77bcf86cd799439011"
    repository.select_by_object_id(test_id)

    mock_collection.find_one.assert_called_once_with(
        {"_id": ObjectId(test_id)}
    )


def test_edit_registry(mock_repository):
    repository, mock_collection = mock_repository

    repository.edit_registry()
    mock_collection.update_one.assert_called_once()


def test_edit_many_registries(mock_repository):
    repository, mock_collection = mock_repository

    repository.edit_many_registries()
    mock_collection.update_many.assert_called_once()


def test_edit_registry_with_increment(mock_repository):
    repository, mock_collection = mock_repository

    repository.edit_registry_with_increment()
    mock_collection.update_many.assert_called_once()


def test_delete_registry(mock_repository):
    repository, mock_collection = mock_repository

    repository.delete_registry()
    mock_collection.delete_one.assert_called_once()


def test_delete_many_registries(mock_repository):
    repository, mock_collection = mock_repository

    repository.delete_many_registries()
    mock_collection.delete_many.assert_called_once()
