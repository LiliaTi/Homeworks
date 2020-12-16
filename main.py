import requests
import telebot
import os
from dotenv import load_dotenv
import textwrap as tw
import time


URL = 'https://dvmn.org/api/long_polling/'


def get_response(url, headers, params={}):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def send_message(text, bot, tg_chat_id):
    result = tw.dedent(text)
    bot.send_message(tg_chat_id, result)


def main():
    load_dotenv()
    tg_chat_id = os.getenv('TG_CHAT_ID')
    devman_token = 'Token {}'.format(os.getenv('DEVMAN_TOKEN'))
    bot_token = os.getenv('BOT_TOKEN')
    headers = {
        'Authorization': devman_token
    }

    bot = telebot.TeleBot(token=bot_token)

    timestamp = None
    while True:
        params = {'timestamp': timestamp}
        try:
            response = get_response(URL, headers, params)
            if response['status'] == 'timeout':
                timestamp = response['timestamp_to_request']
                continue
            else:
                for attempt in response['new_attempts']:
                    if attempt['is_negative']:
                        text = f'''\
                               У Вас проверили работу "{attempt['lesson_title']}".
                               К сожалению, в работе нашлись ошибки
                               '''
                        send_message(text, bot, tg_chat_id)
                    else:
                        text = f'''\
                                У Вас проверили работу "{attempt['lesson_title']}".
                                Преподавателю всё понравилось, можно приступать к следущему уроку!
                                '''
                        send_message(text, bot, tg_chat_id)
                timestamp = response['last_attempt_timestamp']
        except requests.exceptions.ReadTimeout:
            continue
        except ConnectionError:
            time.sleep(1000)
            continue


if __name__ == '__main__':
    main()
