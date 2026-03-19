"""
Testes para o endpoint POST /activities/{activity_name}/signup
Padrão: Arrange-Act-Assert (AAA)
"""
import pytest


def test_signup_successful(client, clean_app_state):
    """
    Teste: Inscrição bem-sucedida em uma atividade
    Arrange: Atividade válida e email novo
    Act: POST para signup
    Assert: Status 200 e email adicionado aos participantes
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Verificar que participante foi adicionado
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity_name]["participants"]


def test_signup_activity_not_found(client, clean_app_state):
    """
    Teste: Inscrição em atividade inexistente
    Arrange: Nome de atividade inválido
    Act: POST para signup
    Assert: Status 404
    """
    # Arrange
    invalid_activity = "Non Existent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{invalid_activity}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_already_registered(client, clean_app_state):
    """
    Teste: Inscrição duplicada (estudante já registrado)
    Arrange: Estudante já existe em participantes
    Act: POST para signup com mesmo email
    Assert: Status 400
    """
    # Arrange
    activity_name = "Chess Club"
    # michael@mergington.edu já está em Chess Club por padrão
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_adds_participant(client, clean_app_state):
    """
    Teste: Validar que participante é efetivamente adicionado
    Arrange: Contar participantes antes
    Act: POST para signup
    Assert: Count aumentou em 1
    """
    # Arrange
    activity_name = "Programming Class"
    email = "newsignup@mergington.edu"

    # Contar participantes antes
    before_response = client.get("/activities")
    before_count = len(before_response.json()[activity_name]["participants"])

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert signup_response.status_code == 200

    # Verificar count após
    after_response = client.get("/activities")
    after_count = len(after_response.json()[activity_name]["participants"])
    assert after_count == before_count + 1
