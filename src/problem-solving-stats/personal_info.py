import os
import configparser

NAME = 0
BAEKJUN_ID = 1
PHONE_NUMBER = 2
EMAIL = 3

lib_dir = os.path.dirname(__file__)
env_config = configparser.ConfigParser()
env_config.read(lib_dir + '/personal-info.ini')

# login
login_id = env_config['LOGIN']['ID']
login_pwd = env_config['LOGIN']['PWD']

# raw datas
list_of_datas = []
list_of_datas.append(env_config['SUBSCRIBER']['member1'].split())
# list_of_datas.append(env_config['SUBSCRIBER']['member2'].split())