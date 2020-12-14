import requests
import telebot
import os
from dotenv import load_dotenv


URL = 'https://dvmn.org/api/long_polling/'


def get_response(url, headers, params={}):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    chat_id = os.getenv('CHAT_ID')
    devman_token = 'Token {}'.format(os.getenv('DEVMAN_TOKEN'))
    bot_token = os.getenv('BOT_TOKEN')
    headers = {
        'Authorization': devman_token
    }

    bot = telebot.TeleBot(token=bot_token)

    try:
        response = get_response(URL, headers)
        for attempt in response['new_attempts']:
            if attempt['is_negative']:
                result = f'''У Вас проверили работу "{attempt['lesson_title']}".
    К сожалению, в работе нашлись ошибки'''
                bot.send_message(chat_id, result)
            else:
                result = f'''У Вас проверили работу "{attempt['lesson_title']}".
    Преподавателю всё понравилось, можно приступать к следущему уроку!'''
                bot.send_message(chat_id, result)
    except requests.exceptions.ReadTimeout:
        response = get_response(URL, headers)
        for attempt in response['new_attempts']:
            if attempt['is_negative']:
                result = f'''У Вас проверили работу "{attempt['lesson_title']}".
                К сожалению, в работе нашлись ошибки'''
                bot.send_message(chat_id, result)
            else:
                result = f'''У Вас проверили работу "{attempt['lesson_title']}".
    Преподавателю всё понравилось, можно приступать к следущему уроку!'''
                bot.send_message(chat_id, result)
    except ConnectionError:
        response = get_response(URL, headers)
        for attempt in response['new_attempts']:
            if attempt['is_negative']:
                result = f'''У Вас проверили работу "{attempt['lesson_title']}".
    К сожалению, в работе нашлись ошибки'''
                bot.send_message(chat_id, result)
            else:
                result = f'''У Вас проверили работу "{attempt['lesson_title']}".
    Преподавателю всё понравилось, можно приступать к следущему уроку!'''
                bot.send_message(chat_id, result)
    timestamp = response['new_attempts'][0]['timestamp']
    while True:
        params = {'timestamp': timestamp}
        try:
            response = get_response(URL, headers, params)
            for attempt in response['new_attempts']:
                if attempt['is_negative']:
                    result = f'''У Вас проверили работу "{attempt['lesson_title']}".
    К сожалению, в работе нашлись ошибки'''
                    bot.send_message(chat_id, result)
                else:
                    result = f'''У Вас проверили работу "{attempt['lesson_title']}".
    Преподавателю всё понравилось, можно приступать к следущему уроку!'''
                    bot.send_message(chat_id, result)
        except requests.exceptions.ReadTimeout:
            response = get_response(URL, headers, params)
            for attempt in response['new_attempts']:
                if attempt['is_negative']:
                    result = f'''У Вас проверили работу "{attempt['lesson_title']}".
    К сожалению, в работе нашлись ошибки'''
                    bot.send_message(chat_id, result)
                else:
                    result = f'''У Вас проверили работу "{attempt['lesson_title']}".
    Преподавателю всё понравилось, можно приступать к следущему уроку!'''
                    bot.send_message(chat_id, result)
        except ConnectionError:
            response = get_response(URL, headers, params)
            for attempt in response['new_attempts']:
                if attempt['is_negative']:
                    result = f'''У Вас проверили работу "{attempt['lesson_title']}".
    К сожалению, в работе нашлись ошибки'''
                    bot.send_message(chat_id, result)
                else:
                    result = f'''У Вас проверили работу "{attempt['lesson_title']}".
    Преподавателю всё понравилось, можно приступать к следущему уроку!'''
                    bot.send_message(chat_id, result)


if __name__ == '__main__':
    main()
