import crawling
import send_alarm
import log
import logging

if __name__ == '__main__':
    log.setup_logger('log/problem-solving-stats.log')
    logging.info('start program!!')

    # session = crawling.login()
    session = None
    # if session != None:
    msg_datas = crawling.crawling(session)
    if msg_datas != None:
        send_alarm.send_alarm(msg_datas)