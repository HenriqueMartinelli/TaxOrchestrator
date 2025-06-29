import pytest
from fastapi.testclient import TestClient
import mongomock

from app.main import app
from app.core import config as config_module  


@pytest.fixture(autouse=True)
def mongo_mock(monkeypatch):
    """
    Substitui o MongoClient por um mongomock, para não precisar do Mongo real.
    Ajusta settings para evitar poluição de banco real.
    """
    mock_client = mongomock.MongoClient()

    monkeypatch.setattr(
        "app.infrastructure.database.mongo.orders_repository.MongoClient",
        lambda *args, **kwargs: mock_client
    )
    monkeypatch.setenv("MONGODB_URL", "mongodb://fake")
    monkeypatch.setenv("MONGODB_DB", "testdb")
    monkeypatch.setenv("TAX_RATES_FILE", "test_tax_rates.json")

    config_module.settings = config_module.Settings()
    yield


@pytest.fixture
def client():
    """TestClient para sua FastAPI app."""
    return TestClient(app)
