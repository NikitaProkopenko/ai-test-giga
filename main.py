"""
GigaChat API client — использует официальный SDK gigachat.
Документация: https://developers.sber.ru/docs/ru/gigachat/api/python-library
"""

import os
import sys
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

load_dotenv()


def get_config() -> dict:
    credentials = os.getenv("GIGACHAT_CREDENTIALS")
    if not credentials:
        print("Ошибка: переменная GIGACHAT_CREDENTIALS не задана.")
        print("Скопируйте .env.example в .env и укажите свои учётные данные.")
        sys.exit(1)

    return {
        "credentials": credentials,
        "scope": os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS"),
        "model": os.getenv("GIGACHAT_MODEL", "GigaChat"),
    }


def send_message(client: GigaChat, model: str, user_message: str) -> str:
    payload = Chat(
        messages=[
            Messages(role=MessagesRole.USER, content=user_message),
        ],
        temperature=0.7,
        model=model,
    )
    response = client.chat(payload)
    return response.choices[0].message.content


def interactive_session(client: GigaChat, model: str) -> None:
    """Интерактивный диалог с GigaChat в терминале."""
    history: list[Messages] = []

    print(f"\nGigaChat ({model}) готов к диалогу.")
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

        history.append(Messages(role=MessagesRole.USER, content=user_input))

        payload = Chat(
            messages=history,
            temperature=0.7,
            model=model,
        )

        try:
            response = client.chat(payload)
            answer = response.choices[0].message.content
            history.append(Messages(role=MessagesRole.ASSISTANT, content=answer))
            print(f"\nGigaChat: {answer}\n")
        except Exception as exc:
            print(f"\nОшибка при запросе к GigaChat: {exc}\n")


def main() -> None:
    config = get_config()

    with GigaChat(
        credentials=config["credentials"],
        scope=config["scope"],
        verify_ssl_certs=False,
    ) as client:
        # Одиночный запрос для демонстрации
        demo_question = "Привет! Расскажи о себе в двух предложениях."
        print(f"Демо-запрос: {demo_question}")
        print("-" * 50)

        try:
            answer = send_message(client, config["model"], demo_question)
            print(f"GigaChat: {answer}")
        except Exception as exc:
            print(f"Ошибка: {exc}")
            sys.exit(1)

        print("-" * 50)

        # Переход в интерактивный режим
        interactive_session(client, config["model"])


if __name__ == "__main__":
    main()
