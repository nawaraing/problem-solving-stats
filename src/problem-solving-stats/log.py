import logging

def setup_logger(log_file):
    # 로그 파일 설정
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='[%(asctime)19.19s][%(name)15.15s][%(levelname)8.8s] %(message)s')

    # # 로그 메시지 출력
    # logging.debug('This is a debug message')
    # logging.info('This is an info message')
    # logging.warning('This is a warning message')
    # logging.error('This is an error message')
    # logging.critical('This is a critical message')
