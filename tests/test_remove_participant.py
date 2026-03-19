"""
Testes para o endpoint DELETE /activities/{activity_name}/participants
Padrão: Arrange-Act-Assert (AAA)
"""
import pytest


def test_remove_participant_successful(client, clean_app_state):
    """
    Teste: Remoção bem-sucedida de participante
    Arrange: Participante existe na atividade
    Act: DELETE para remover
    Assert: Status 200 e participante removido
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Já existe em Chess Club

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]

    # Verificar que participante foi removido
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email not in activities_data[activity_name]["participants"]


def test_remove_participant_activity_not_found(client, clean_app_state):
    """
    Teste: Remoção de atividade inexistente
    Arrange: Nome de atividade inválido
    Act: DELETE para remover
    Assert: Status 404
    """
    # Arrange
    invalid_activity = "Non Existent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{invalid_activity}/participants", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_participant_not_found(client, clean_app_state):
    """
    Teste: Remoção de participante que não existe na atividade
    Arrange: Email não existe em participantes
    Act: DELETE para remover
    Assert: Status 404
    """
    # Arrange
    activity_name = "Basketball Team"
    email = "nonexistent@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_remove_participant_validates_removal(client, clean_app_state):
    """
    Teste: Validar que participante é efetivamente removido
    Arrange: Contar participantes antes
    Act: DELETE para remover
    Assert: Count diminuiu em 1
    """
    # Arrange
    activity_name = "Drama Club"
    email = "noah@mergington.edu"  # Já existe em Drama Club

    # Contar participantes antes
    before_response = client.get("/activities")
    before_count = len(before_response.json()[activity_name]["participants"])

    # Act
    remove_response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )

    # Assert
    assert remove_response.status_code == 200

    # Verificar count após
    after_response = client.get("/activities")
    after_count = len(after_response.json()[activity_name]["participants"])
    assert after_count == before_count - 1
