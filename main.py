import requests
import telebot
import os
from dotenv import load_dotenv
import textwrap as tw


URL = 'https://dvmn.org/api/long_polling/'


def get_response(url, headers, params={}):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


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
            for attempt in response['new_attempts']:
                if attempt['is_negative']:
                    text = f'''\
                    	 У Вас проверили работу "{attempt['lesson_title']}".
                         К сожалению, в работе нашлись ошибки
                        '''
                    result = tw.dedent(text)
                    bot.send_message(tg_chat_id, result)
                else:
                    text =  f'''\
                    	У Вас проверили работу "{attempt['lesson_title']}".
                        Преподавателю всё понравилось, можно приступать к следущему уроку!
                        '''
                    result = tw.dedent(text)
                    bot.send_message(tg_chat_id, result)
            timestamp = response['new_attempts'][0]['timestamp']
        except requests.exceptions.ReadTimeout:
            continue
        except ConnectionError:
            continue


if __name__ == '__main__':
    main()
