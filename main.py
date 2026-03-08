import os
import sys
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

load_dotenv()


def main() -> None:
    credentials = os.getenv("GIGACHAT_CREDENTIALS")
    if not credentials:
        print("Ошибка: укажите GIGACHAT_CREDENTIALS в файле .env")
        sys.exit(1)

    history: list[Messages] = []

    with GigaChat(credentials=credentials, scope="GIGACHAT_API_PERS", verify_ssl_certs=False) as client:
        print("GigaChat готов. Введите ваш вопрос (для выхода — 'exit').\n")

        while True:
            user_input = input("Вы: ").strip()

            if not user_input:
                continue
            if user_input.lower() == "exit":
                break

            history.append(Messages(role=MessagesRole.USER, content=user_input))

            response = client.chat(Chat(messages=history))
            answer = response.choices[0].message.content

            history.append(Messages(role=MessagesRole.ASSISTANT, content=answer))
            print(f"\nGigaChat: {answer}\n")


if __name__ == "__main__":
    main()
