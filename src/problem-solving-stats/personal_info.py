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
list_of_datas.append(env_config['SUBSCRIBER']['member2'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member3'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member4'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member5'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member6'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member7'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member8'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member9'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member10'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member11'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member12'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member13'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member14'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member15'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member16'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member17'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member18'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member19'].split())
list_of_datas.append(env_config['SUBSCRIBER']['member20'].split())