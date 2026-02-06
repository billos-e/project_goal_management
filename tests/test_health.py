"""Tests for health check endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock


def test_health_check(client: TestClient):
    """Test simple health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_detailed_health_check_success(client: TestClient):
    """Test detailed health check with successful database connection."""
    with patch("app.services.database.database_service.health_check", new_callable=AsyncMock) as mock_health:
        mock_health.return_value = True
        
        response = client.get("/health/detailed")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["components"]["api"] == "ok"
        assert data["components"]["database"] == "ok"
        assert data["components"]["database_error"] is None


def test_detailed_health_check_database_failure(client: TestClient):
    """Test detailed health check with database connection failure."""
    with patch("app.services.database.database_service.health_check", new_callable=AsyncMock) as mock_health:
        mock_health.return_value = False
        
        response = client.get("/health/detailed")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "degraded"
        assert data["components"]["api"] == "ok"
        assert data["components"]["database"] == "failed"
        assert data["components"]["database_error"] == "Connection failed"
