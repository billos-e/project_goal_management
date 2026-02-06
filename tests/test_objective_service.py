"""Tests for objective parsing."""
from app.services.objectives import objective_service


def test_parse_objective_without_token():
    parsed = objective_service._parse_objective(
        "Finish report tomorrow 5pm",
        "Europe/Paris",
    )
    assert parsed is not None
    assert parsed.title == "Finish report"


def test_parse_objective_today():
    parsed = objective_service._parse_objective(
        "Finish report today 18h",
        "Europe/Paris",
    )
    assert parsed is not None
    assert parsed.title == "Finish report"


def test_parse_objective_date():
    parsed = objective_service._parse_objective(
        "Finish report 07/02 17h",
        "Europe/Paris",
    )
    assert parsed is not None
    assert parsed.title == "Finish report"
