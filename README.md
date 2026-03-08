# GigaChat API — Python Client

Два варианта подключения к [GigaChat API](https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/gigachat-api):

| Файл | Описание |
|---|---|
| `main.py` | Использует официальный SDK `gigachat` |
| `gigachat_raw.py` | Прямые HTTP-запросы, без SDK |

## Быстрый старт

### 1. Получить учётные данные

Зарегистрируйтесь на [developers.sber.ru](https://developers.sber.ru/studio/) и создайте проект GigaChat API. Скопируйте **Authorization Key** (Base64-строку).

### 2. Настроить окружение

```bash
cp .env.example .env
```

Откройте `.env` и вставьте свой ключ:

```dotenv
GIGACHAT_CREDENTIALS=ваш_ключ_авторизации
GIGACHAT_SCOPE=GIGACHAT_API_PERS   # для физ. лиц
GIGACHAT_MODEL=GigaChat
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Запустить

**Вариант 1 — через SDK (рекомендуется):**

```bash
python main.py
```

**Вариант 2 — прямые HTTP-запросы:**

```bash
python gigachat_raw.py
```

## Как это работает

```
Запрос пользователя
       │
       ▼
 OAuth 2.0 токен ──► ngw.devices.sberbank.ru:9443/api/v2/oauth
       │
       ▼
Chat Completions ──► gigachat.devices.sberbank.ru/api/v1/chat/completions
       │
       ▼
  Ответ в терминал
```

1. Клиент получает временный OAuth-токен (действует 30 минут).
2. С токеном отправляет сообщение в Chat Completions API.
3. Ответ модели выводится в терминал.
4. История диалога сохраняется для поддержки контекста.

## Переменные окружения

| Переменная | Обязательная | Описание |
|---|---|---|
| `GIGACHAT_CREDENTIALS` | Да | Base64-ключ из личного кабинета Sber |
| `GIGACHAT_SCOPE` | Нет | `GIGACHAT_API_PERS` (физ. лица) / `GIGACHAT_API_B2B` (бизнес) |
| `GIGACHAT_MODEL` | Нет | `GigaChat`, `GigaChat-Plus` или `GigaChat-Pro` |

## Примечание об SSL

GigaChat использует российский сертификат Минцифры, который не входит в стандартные CA-хранилища. В коде используется `verify_ssl_certs=False` для обхода этого ограничения. В продакшне рекомендуется добавить сертификат в доверенные.
