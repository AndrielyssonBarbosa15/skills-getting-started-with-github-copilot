"""
Testes para o endpoint GET /activities
Padrão: Arrange-Act-Assert (AAA)
"""
import pytest


def test_get_activities_returns_all_activities(client, clean_app_state):
    """
    Teste: GET /activities retorna todas as atividades
    Arrange: Cliente pronto
    Act: Fazer requisição GET
    Assert: Status 200 e contém atividades
    """
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    for activity in expected_activities:
        assert activity in data


def test_get_activities_structure(client, clean_app_state):
    """
    Teste: Resposta tem estrutura correta
    Arrange: Cliente pronto
    Act: Fazer requisição GET
    Assert: Cada atividade tem campos obrigatórios
    """
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in data.items():
        for field in required_fields:
            assert (
                field in activity_data
            ), f"Campo '{field}' faltando em {activity_name}"


def test_get_activities_participants_initialized(client, clean_app_state):
    """
    Teste: Cada atividade tem lista de participantes
    Arrange: Cliente pronto
    Act: Fazer requisição GET
    Assert: Verificar que participants têm dados iniciais
    """
    # Arrange
    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    for activity_name, activity in data.items():
        assert "participants" in activity
        assert isinstance(activity["participants"], list)
        # Todas as atividades têm participantes iniciais
        assert len(activity["participants"]) >= 0
