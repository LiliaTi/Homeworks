import requests
import telebot
import os
import textwrap as tw
import time
import logging


URL = 'https://dvmn.org/api/long_polling/'


def get_response(url, headers, params={}):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def main():
    tg_chat_id = os.environ.get('TG_CHAT_ID')
    devman_token = 'Token {}'.format(os.environ.get('DEVMAN_TOKEN'))
    bot_token = os.environ.get('BOT_TOKEN')
    headers = {
        'Authorization': devman_token
    }

    bot = telebot.TeleBot(token=bot_token)

    class MyLogsHandler(logging.Handler):

        def emit(self, record):
            logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
            log_entry = self.format(record)
            bot.send_message(tg_chat_id, log_entry)

    logger = logging.getLogger("Bot logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    
    logger.info('Привет, я - логер')

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
                    else:
                        text = f'''\
                                У Вас проверили работу "{attempt['lesson_title']}".
                                Преподавателю всё понравилось, можно приступать к следущему уроку!
                                '''
                result = tw.dedent(text)
                bot.send_message(tg_chat_id, result)
                timestamp = response['last_attempt_timestamp']
        except requests.exceptions.ReadTimeout:
            continue
        except ConnectionError:
            time.sleep(1000)
            continue


if __name__ == '__main__':
    main()
