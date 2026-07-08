import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_listar_tarefas(client):
    with patch("app.get_connection") as mock_conn:
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(1, "Estudar Docker", False)]
        mock_conn.return_value.cursor.return_value = mock_cursor

        response = client.get("/api/tarefas")
        assert response.status_code == 200
        data = response.get_json()
        assert data[0]["titulo"] == "Estudar Docker"

def test_criar_tarefa(client):
    with patch("app.get_connection") as mock_conn:
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1]
        mock_conn.return_value.cursor.return_value = mock_cursor

        response = client.post("/api/tarefas", json={"titulo": "Nova tarefa"})
        assert response.status_code == 201
        data = response.get_json()
        assert data["titulo"] == "Nova tarefa"

def test_deletar_tarefa(client):
    with patch("app.get_connection") as mock_conn:
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor

        response = client.delete("/api/tarefas/1")
        assert response.status_code == 200