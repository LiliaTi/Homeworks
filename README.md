# Отправка уведомлений о проверке работ от [dvmn.org](https://dvmn.org/modules/)

Данный скрипт автоматически отправляет пользователю в телеграм информацию о проверенных работах на [Девмане](https://dvmn.org/modules/)

## Как установить

Создайте в корне проекта файл `.env` и заполните Ваши данные: токен авторизации на [Девмане](https://dvmn.org/modules/), токен Вашего телеграм-бота, Ваш chat_id в телеграм.

```python
DEVMAN_TOKEN=YOUR_DEVMAN_TOKEN
BOT_TOKEN=YOUR_BOT_TOKEN
TG_CHAT_ID=YOUR_TG_CHAT_ID
```

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:

```python
pip install -r requirements.txt
```

## Как запустить 

Введите в консоль следущую команду:

```python
python main.py
```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org.](https://dvmn.org/modules/)

