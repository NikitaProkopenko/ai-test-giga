# GigaChat API — Python Client

Консольный чат с GigaChat через официальный Python SDK.

## Быстрый старт

### 1. Получить ключ авторизации

Зарегистрируйтесь на [developers.sber.ru](https://developers.sber.ru/studio/), создайте проект GigaChat API и скопируйте **Authorization Key**.

### 2. Настроить окружение

```bash
cp .env.example .env
```

Откройте `.env` и вставьте свой ключ:

```dotenv
GIGACHAT_CREDENTIALS=ваш_ключ_авторизации
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Запустить

```bash
python main.py
```

### 5. Проверить доступность API и актуальность токена

```bash
pytest test_gigachat_api.py -v
```

Тесты проверяют:
- наличие `GIGACHAT_CREDENTIALS` в окружении или `.env`
- получение действительного OAuth-токена (credentials не истекли)
- доступность API (запрос списка моделей возвращает непустой ответ)

При отсутствии `GIGACHAT_CREDENTIALS` интеграционные тесты пропускаются (`SKIPPED`), а не падают с ошибкой.

### Пример диалога

```
GigaChat готов. Введите ваш вопрос (для выхода — 'exit').

Вы: Какая погода?

GigaChat: Я не имею доступа к данным о текущей погоде...

Вы: exit
```
