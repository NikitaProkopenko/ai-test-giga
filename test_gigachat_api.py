"""Integration tests: availability of the GigaChat API and validity of the token.

Run:
    pytest test_gigachat_api.py -v
"""

import os
import time

import pytest
from dotenv import load_dotenv

load_dotenv()

_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")
_SCOPE = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")

_requires_credentials = pytest.mark.skipif(
    not _CREDENTIALS,
    reason="GIGACHAT_CREDENTIALS не задан — пропускаем интеграционный тест.",
)


def _make_client():
    from gigachat import GigaChat

    return GigaChat(credentials=_CREDENTIALS, scope=_SCOPE, verify_ssl_certs=False)


# ---------------------------------------------------------------------------
# 1. Credentials presence
# ---------------------------------------------------------------------------


def test_credentials_present():
    """GIGACHAT_CREDENTIALS must be set and non-empty."""
    assert _CREDENTIALS, (
        "GIGACHAT_CREDENTIALS не задан. "
        "Укажите его в .env или в переменной окружения."
    )
    assert _CREDENTIALS.strip(), "GIGACHAT_CREDENTIALS задан, но пустой."


# ---------------------------------------------------------------------------
# 2. Token validity
# ---------------------------------------------------------------------------


@_requires_credentials
def test_token_is_valid():
    """A valid OAuth token must be obtainable with the provided credentials."""
    with _make_client() as client:
        token = client.get_token()

    assert token is not None, (
        "get_token() вернул None — возможно, credentials не переданы клиенту."
    )
    assert token.access_token, (
        "access_token пустой — credentials недействительны или истёк срок действия."
    )

    # expires_at is a Unix timestamp in milliseconds
    now_ms = int(time.time() * 1000)
    assert token.expires_at > now_ms, (
        f"Токен уже истёк: expires_at={token.expires_at}, now={now_ms}. "
        "Обновите GIGACHAT_CREDENTIALS."
    )


# ---------------------------------------------------------------------------
# 3. API availability
# ---------------------------------------------------------------------------


@_requires_credentials
def test_api_is_available():
    """GigaChat API must respond to a models listing request."""
    with _make_client() as client:
        models = client.get_models()

    assert models is not None, "get_models() вернул None — API недоступен."
    assert len(models.data) > 0, (
        "API вернул пустой список моделей — возможно, проблема с авторизацией или scope."
    )
