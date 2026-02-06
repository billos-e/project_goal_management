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
    ) as upsert_mock, patch(
        "app.services.nlu.nlu_service.identify_intent",
        new_callable=AsyncMock,
    ) as nlu_mock:
        typing_mock.return_value = True
        send_mock.return_value = True
        upsert_mock.return_value = True
        nlu_mock.return_value = {
            "intent": "greet",
            "response_text": "Salut, humain.",
            "source": "gemini",
        }

        response = client.post(
            "/telegram/webhook/test-token",
            json=_make_update(),
            headers={"X-Telegram-Bot-Api-Secret-Token": "test-secret"},
        )

        assert response.status_code == 200
        typing_mock.assert_awaited_once()
        send_mock.assert_awaited_once()
        upsert_mock.assert_awaited_once()
        nlu_mock.assert_awaited_once()


def test_webhook_self_test(client: TestClient):
    """/self_test should call diagnostics and send status message."""
    settings.telegram_webhook_secret = "test-secret"
    settings.telegram_bot_token = "test-token"

    update = _make_update()
    update["message"]["text"] = "/self_test"

    with patch(
        "app.services.telegram.telegram_service.send_typing_indicator",
        new_callable=AsyncMock,
    ) as typing_mock, patch(
        "app.services.telegram.telegram_service.send_message",
        new_callable=AsyncMock,
    ) as send_mock, patch(
        "app.services.database.database_service.upsert_user",
        new_callable=AsyncMock,
    ) as upsert_mock, patch(
        "app.services.database.database_service.health_check",
        new_callable=AsyncMock,
    ) as db_mock, patch(
        "app.services.nlu.nlu_service.health_check",
        new_callable=AsyncMock,
    ) as gemini_mock:
        typing_mock.return_value = True
        send_mock.return_value = True
        upsert_mock.return_value = True
        db_mock.return_value = True
        gemini_mock.return_value = (True, None)

        response = client.post(
            "/telegram/webhook/test-token",
            json=update,
            headers={"X-Telegram-Bot-Api-Secret-Token": "test-secret"},
        )

        assert response.status_code == 200
        typing_mock.assert_awaited_once()
        send_mock.assert_awaited_once()
        upsert_mock.assert_awaited_once()
        db_mock.assert_awaited_once()
        gemini_mock.assert_awaited_once()


def test_webhook_self_test_database_failure(client: TestClient):
    """/self_test should report DB failure."""
    settings.telegram_webhook_secret = "test-secret"
    settings.telegram_bot_token = "test-token"

    update = _make_update()
    update["message"]["text"] = "/self_test"

    with patch(
        "app.services.telegram.telegram_service.send_typing_indicator",
        new_callable=AsyncMock,
    ) as typing_mock, patch(
        "app.services.telegram.telegram_service.send_message",
        new_callable=AsyncMock,
    ) as send_mock, patch(
        "app.services.database.database_service.upsert_user",
        new_callable=AsyncMock,
    ) as upsert_mock, patch(
        "app.services.database.database_service.health_check",
        new_callable=AsyncMock,
    ) as db_mock, patch(
        "app.services.nlu.nlu_service.health_check",
        new_callable=AsyncMock,
    ) as gemini_mock:
        typing_mock.return_value = True
        send_mock.return_value = True
        upsert_mock.return_value = True
        db_mock.return_value = False
        gemini_mock.return_value = (True, None)

        response = client.post(
            "/telegram/webhook/test-token",
            json=update,
            headers={"X-Telegram-Bot-Api-Secret-Token": "test-secret"},
        )

        assert response.status_code == 200
        typing_mock.assert_awaited_once()
        send_mock.assert_awaited_once()
        upsert_mock.assert_awaited_once()
        db_mock.assert_awaited_once()
        gemini_mock.assert_awaited_once()
        assert "DB" in send_mock.call_args.args[1]
        assert "❌" in send_mock.call_args.args[1]


def test_webhook_self_test_gemini_failure(client: TestClient):
    """/self_test should report Gemini failure."""
    settings.telegram_webhook_secret = "test-secret"
    settings.telegram_bot_token = "test-token"

    update = _make_update()
    update["message"]["text"] = "/self_test"

    with patch(
        "app.services.telegram.telegram_service.send_typing_indicator",
        new_callable=AsyncMock,
    ) as typing_mock, patch(
        "app.services.telegram.telegram_service.send_message",
        new_callable=AsyncMock,
    ) as send_mock, patch(
        "app.services.database.database_service.upsert_user",
        new_callable=AsyncMock,
    ) as upsert_mock, patch(
        "app.services.database.database_service.health_check",
        new_callable=AsyncMock,
    ) as db_mock, patch(
        "app.services.nlu.nlu_service.health_check",
        new_callable=AsyncMock,
    ) as gemini_mock:
        typing_mock.return_value = True
        send_mock.return_value = True
        upsert_mock.return_value = True
        db_mock.return_value = True
        gemini_mock.return_value = (False, "Gemini down")

        response = client.post(
            "/telegram/webhook/test-token",
            json=update,
            headers={"X-Telegram-Bot-Api-Secret-Token": "test-secret"},
        )

        assert response.status_code == 200
        typing_mock.assert_awaited_once()
        send_mock.assert_awaited_once()
        upsert_mock.assert_awaited_once()
        db_mock.assert_awaited_once()
        gemini_mock.assert_awaited_once()
        assert "Gemini" in send_mock.call_args.args[1]
        assert "❌" in send_mock.call_args.args[1]


def test_webhook_new_habit_command(client: TestClient):
    """new habit command should create habit and bypass NLU."""
    settings.telegram_webhook_secret = "test-secret"
    settings.telegram_bot_token = "test-token"

    update = _make_update()
    update["message"]["text"] = "new habit: Drink water"

    with patch(
        "app.services.telegram.telegram_service.send_typing_indicator",
        new_callable=AsyncMock,
    ) as typing_mock, patch(
        "app.services.telegram.telegram_service.send_message",
        new_callable=AsyncMock,
    ) as send_mock, patch(
        "app.services.database.database_service.upsert_user",
        new_callable=AsyncMock,
    ) as upsert_mock, patch(
        "app.routes.telegram_webhook.habit_service.create_habit",
        new_callable=AsyncMock,
    ) as create_mock, patch(
        "app.routes.telegram_webhook.nlu_service.identify_intent",
        new_callable=AsyncMock,
    ) as nlu_mock:
        typing_mock.return_value = True
        send_mock.return_value = True
        upsert_mock.return_value = True
        create_mock.return_value = (True, "Habitude enregistrée.")

        response = client.post(
            "/telegram/webhook/test-token",
            json=update,
            headers={"X-Telegram-Bot-Api-Secret-Token": "test-secret"},
        )

        assert response.status_code == 200
        typing_mock.assert_awaited_once()
        send_mock.assert_awaited_once()
        upsert_mock.assert_awaited_once()
        create_mock.assert_awaited_once_with(123456, "Drink water")
        nlu_mock.assert_not_awaited()


def test_webhook_show_habits_command(client: TestClient):
    """show habits should list habits and bypass NLU."""
    settings.telegram_webhook_secret = "test-secret"
    settings.telegram_bot_token = "test-token"

    update = _make_update()
    update["message"]["text"] = "show habits"

    with patch(
        "app.services.telegram.telegram_service.send_typing_indicator",
        new_callable=AsyncMock,
    ) as typing_mock, patch(
        "app.services.telegram.telegram_service.send_message",
        new_callable=AsyncMock,
    ) as send_mock, patch(
        "app.services.database.database_service.upsert_user",
        new_callable=AsyncMock,
    ) as upsert_mock, patch(
        "app.routes.telegram_webhook.habit_service.list_habits",
        new_callable=AsyncMock,
    ) as list_mock, patch(
        "app.routes.telegram_webhook.habit_service.format_habit_list",
    ) as format_mock, patch(
        "app.routes.telegram_webhook.nlu_service.identify_intent",
        new_callable=AsyncMock,
    ) as nlu_mock:
        typing_mock.return_value = True
        send_mock.return_value = True
        upsert_mock.return_value = True
        list_mock.return_value = [{"title": "Drink water", "frequency_type": "daily"}]
        format_mock.return_value = "1. Drink water — daily"

        response = client.post(
            "/telegram/webhook/test-token",
            json=update,
            headers={"X-Telegram-Bot-Api-Secret-Token": "test-secret"},
        )

        assert response.status_code == 200
        typing_mock.assert_awaited_once()
        send_mock.assert_awaited_once()
        upsert_mock.assert_awaited_once()
        list_mock.assert_awaited_once_with(123456)
        format_mock.assert_called_once()
        nlu_mock.assert_not_awaited()


def test_webhook_new_goal_command(client: TestClient):
    """new goal command should create objective and bypass NLU."""
    settings.telegram_webhook_secret = "test-secret"
    settings.telegram_bot_token = "test-token"

    update = _make_update()
    update["message"]["text"] = "new goal: Finish report by tomorrow 5pm"

    with patch(
        "app.services.telegram.telegram_service.send_typing_indicator",
        new_callable=AsyncMock,
    ) as typing_mock, patch(
        "app.services.telegram.telegram_service.send_message",
        new_callable=AsyncMock,
    ) as send_mock, patch(
        "app.services.database.database_service.upsert_user",
        new_callable=AsyncMock,
    ) as upsert_mock, patch(
        "app.routes.telegram_webhook.objective_service.create_objective",
        new_callable=AsyncMock,
    ) as create_mock, patch(
        "app.routes.telegram_webhook.nlu_service.identify_intent",
        new_callable=AsyncMock,
    ) as nlu_mock:
        typing_mock.return_value = True
        send_mock.return_value = True
        upsert_mock.return_value = True
        create_mock.return_value = (True, "Objectif enregistré.")

        response = client.post(
            "/telegram/webhook/test-token",
            json=update,
            headers={"X-Telegram-Bot-Api-Secret-Token": "test-secret"},
        )

        assert response.status_code == 200
        typing_mock.assert_awaited_once()
        send_mock.assert_awaited_once()
        upsert_mock.assert_awaited_once()
        create_mock.assert_awaited_once_with(123456, "Finish report by tomorrow 5pm")
        nlu_mock.assert_not_awaited()


def test_webhook_show_goals_command(client: TestClient):
    """show goals should list objectives and bypass NLU."""
    settings.telegram_webhook_secret = "test-secret"
    settings.telegram_bot_token = "test-token"

    update = _make_update()
    update["message"]["text"] = "show goals"

    with patch(
        "app.services.telegram.telegram_service.send_typing_indicator",
        new_callable=AsyncMock,
    ) as typing_mock, patch(
        "app.services.telegram.telegram_service.send_message",
        new_callable=AsyncMock,
    ) as send_mock, patch(
        "app.services.database.database_service.upsert_user",
        new_callable=AsyncMock,
    ) as upsert_mock, patch(
        "app.routes.telegram_webhook.objective_service.list_objectives",
        new_callable=AsyncMock,
    ) as list_mock, patch(
        "app.routes.telegram_webhook.objective_service.get_user_timezone",
        new_callable=AsyncMock,
    ) as timezone_mock, patch(
        "app.routes.telegram_webhook.objective_service.format_objective_list",
    ) as format_mock, patch(
        "app.routes.telegram_webhook.nlu_service.identify_intent",
        new_callable=AsyncMock,
    ) as nlu_mock:
        typing_mock.return_value = True
        send_mock.return_value = True
        upsert_mock.return_value = True
        list_mock.return_value = [{"title": "Finish report", "deadline": "2026-02-07T16:00:00+00:00"}]
        timezone_mock.return_value = "Europe/Paris"
        format_mock.return_value = "1. Finish report — 07/02/2026 17:00"

        response = client.post(
            "/telegram/webhook/test-token",
            json=update,
            headers={"X-Telegram-Bot-Api-Secret-Token": "test-secret"},
        )

        assert response.status_code == 200
        typing_mock.assert_awaited_once()
        send_mock.assert_awaited_once()
        upsert_mock.assert_awaited_once()
        list_mock.assert_awaited_once_with(123456)
        timezone_mock.assert_awaited_once_with(123456)
        format_mock.assert_called_once()
        nlu_mock.assert_not_awaited()
