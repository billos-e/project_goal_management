"""Tests for Telegram webhook endpoint."""
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.config import settings


def _make_update():
    return {
        "update_id": 1001,
        "message": {
            "message_id": 10,
            "from": {"id": 123456, "is_bot": False, "first_name": "Billux"},
            "chat": {"id": 123456, "type": "private"},
            "date": 1700000000,
            "text": "Salut TARS",
        },
    }


def test_webhook_missing_secret(client: TestClient):
    """Missing secret should return 401."""
    settings.telegram_webhook_secret = "test-secret"
    settings.telegram_bot_token = "test-token"

    response = client.post(
        "/telegram/webhook/test-token",
        json=_make_update(),
    )

    assert response.status_code == 401


def test_webhook_invalid_secret(client: TestClient):
    """Invalid secret should return 401."""
    settings.telegram_webhook_secret = "test-secret"
    settings.telegram_bot_token = "test-token"

    response = client.post(
        "/telegram/webhook/test-token",
        json=_make_update(),
        headers={"X-Telegram-Bot-Api-Secret-Token": "wrong"},
    )

    assert response.status_code == 401


def test_webhook_valid_secret_sends_response(client: TestClient):
    """Valid secret should process webhook and send response."""
    settings.telegram_webhook_secret = "test-secret"
    settings.telegram_bot_token = "test-token"

    with patch(
        "app.services.telegram.telegram_service.send_typing_indicator",
        new_callable=AsyncMock,
    ) as typing_mock, patch(
        "app.services.telegram.telegram_service.send_message",
        new_callable=AsyncMock,
    ) as send_mock, patch(
        "app.services.database.database_service.upsert_user",
        new_callable=AsyncMock,
    ) as upsert_mock:
        typing_mock.return_value = True
        send_mock.return_value = True
        upsert_mock.return_value = True

        response = client.post(
            "/telegram/webhook/test-token",
            json=_make_update(),
            headers={"X-Telegram-Bot-Api-Secret-Token": "test-secret"},
        )

        assert response.status_code == 200
        typing_mock.assert_awaited_once()
        send_mock.assert_awaited_once()
        upsert_mock.assert_awaited_once()