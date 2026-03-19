"""
Fixtures compartilhadas para testes FastAPI
Aqui centralizamos dados de teste e cliente reutilizável
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture que fornece um cliente de teste (TestClient)
    para fazer requisições HTTP contra a aplicação
    """
    return TestClient(app)


@pytest.fixture
def clean_app_state():
    """
    Fixture que reseta o estado da aplicação antes de cada teste
    Garante isolamento entre testes, preservando dados originais
    """
    # Salva estado original (deep copy de cada atividade)
    original_activities = {k: dict(v) for k, v in activities.items()}
    original_participants = {
        k: list(v["participants"]) for k, v in activities.items()
    }

    yield

    # Restaura estado original após teste
    for activity_name in activities:
        activities[activity_name]["participants"] = original_participants[activity_name]


@pytest.fixture
def sample_activity():
    """
    Fixture que fornece dados de uma atividade de teste
    """
    return {
        "name": "Test Activity",
        "description": "An activity for testing",
        "schedule": "Mondays, 3:00 PM - 4:00 PM",
        "max_participants": 10,
        "participants": ["test@example.com"],
    }
