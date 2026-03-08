"""
GigaChat API client — прямые HTTP-запросы без SDK.
Показывает, как работает авторизация OAuth 2.0 и запросы к Chat Completions.
Документация: https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/gigachat-api
"""

import os
import sys
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
CHAT_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"


def get_access_token(credentials: str, scope: str) -> str:
    """Получает временный токен доступа через OAuth 2.0."""
    response = requests.post(
        TOKEN_URL,
        headers={
            "Authorization": f"Basic {credentials}",
            "RqUID": str(uuid.uuid4()),
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"scope": scope},
        verify=False,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def chat_completion(
    token: str,
    model: str,
    messages: list[dict],
    temperature: float = 0.7,
) -> str:
    """Отправляет запрос к Chat Completions и возвращает текст ответа."""
    response = requests.post(
        CHAT_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": messages,
            "temperature": temperature,
        },
        verify=False,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def main() -> None:
    credentials = os.getenv("GIGACHAT_CREDENTIALS")
    if not credentials:
        print("Ошибка: переменная GIGACHAT_CREDENTIALS не задана.")
        print("Скопируйте .env.example в .env и укажите свои учётные данные.")
        sys.exit(1)

    scope = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
    model = os.getenv("GIGACHAT_MODEL", "GigaChat")

    # Отключаем предупреждения об SSL (нужно для сертификата Сбера)
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print("Получаем токен доступа...")
    try:
        token = get_access_token(credentials, scope)
        print("Токен получен успешно.\n")
    except Exception as exc:
        print(f"Ошибка при получении токена: {exc}")
        sys.exit(1)

    history: list[dict] = []

    print(f"GigaChat ({model}) готов к диалогу.")
    print("Введите 'выход' или 'exit' для завершения.\n")

    while True:
        try:
            user_input = input("Вы: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nДо свидания!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("выход", "exit", "quit"):
            print("До свидания!")
            break

        history.append({"role": "user", "content": user_input})

        try:
            answer = chat_completion(token, model, history)
            history.append({"role": "assistant", "content": answer})
            print(f"\nGigaChat: {answer}\n")
        except requests.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 401:
                print("Токен истёк, обновляем...")
                try:
                    token = get_access_token(credentials, scope)
                    answer = chat_completion(token, model, history)
                    history.append({"role": "assistant", "content": answer})
                    print(f"\nGigaChat: {answer}\n")
                except Exception as retry_exc:
                    print(f"Ошибка после обновления токена: {retry_exc}\n")
            else:
                print(f"HTTP-ошибка: {exc}\n")
        except Exception as exc:
            print(f"Ошибка: {exc}\n")


if __name__ == "__main__":
    main()
