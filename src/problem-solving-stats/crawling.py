import personal_info
import tier

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

BAEKJUN_URL = 'https://www.acmicpc.net'
RETRY_CNT = 1

# practice_ranking page
SUBMIT_ID = 0
GROUP_RANK = 0
BAEKJUN_ID = 1
PROBLEM_ID = 2
RESULT = 3
MEMORY = 4
TIME = 5
LANGUAGE = 6
CODE_LENGTH = 7
SUBMIT_TIME = 8

# practice page
PRACTICE_NAME = 0
START_DATE = 1
END_DATE = 2

class MsgData:
    def __init__(self):
        self.msg_data_id = 0            # 해당 msg_data의 id

        # member의 개인정보
        self.member_name = ''           # 해당 member의 이름
        self.member_baekjun_id = ''     # 해당 member의 백준 id
        self.member_phone_number = ''   # 해당 member의 전화번호
        self.member_email = ''          # 해당 member의 이메일

        # msg 정보
        self.solve_problem_number = 0   # 금주에 푼 문제 수
        self.number_of_attempt = 0      # 금주에 시도한 횟수

        self.maximum_problem_level = '' # 금주에 푼 가장 어려운 문제

        self.group_top_3 = ''           # 금주에 그룹 상위 3명
        self.group_member_rank = 0      # 금주에 그룹 랭크

        self.solved_member_tier = ''    # solved.ac 티어
        self.solved_member_rating = 0   # solved.ac 레이팅
        self.solved_member_rank = 0     # solved.ac 랭크
    
    def __str__(self):
        return f"MsgData: msg_data_id[{self.msg_data_id}] member_name[{self.member_name}] member_baekjun_id[{self.member_baekjun_id}] member_phone_number[{self.member_phone_number}] member_email[{self.member_email}] solve_problem_number[{self.solve_problem_number}] solved_member_tier[{self.solved_member_tier}] solved_member_rating[{self.solved_member_rating}] solved_member_rank[{self.solved_member_rank}]"

def login():
    logging.info('start login()')

    session = requests.Session()

    # reqests datas
    login_data = {
        'login_user_id': personal_info.login_id,
        'login_password': personal_info.login_pwd,
        'auto_login' : 'on',
        'next' : '/group/practice/20868',
        'stack' : '0',
        # 'g-recaptcha-response' : '03AFcWeA5X_lPxQ-BtwAPv462oKLIgBssLM2UmP-xBUuMV5LJTrjJX_DQmtunY3KiGwCyIvN6NvwXsofnqFkkRaTX5LRIFyzLrp2jd5nP9CcFAe4CGiMqDnpugwcdf0AhAHduID19zsIgOB942pGfOnNwduYtsLzlrfUH3gpghqE3z1_0uAkqtYZ9WY_ScXLabBeYj4zO38tTs6ejcVUiTgMHvOlqIfluDQ9crX7hFruIymL-1m9fUZud2y52r_9vJ9uy309t-kc1iQPd7nM3e8slCDH6Z3kqDRRSpwOjNX__QU0IWOeu-1R4ZT-NmOhpNF_xoqP_65dmTqWQsXkyGtc97FalA008yEaTn4wqcyEqxOG1g339kdBMo-6CnLWF01DHdNDF3s-16zbPR5-JHKR0IZDlz2YQ0VT0jZYaXOVt-xj5dd-RDVjfLrhnrrhWc6Xa0njLwX5ZpvXuOayh_CIM-j38sWnoEbqXkgHCOwAA9deNd2CQK8kQMTz4r5nckXKxdK9IIIa1VY0tRJyQBTBNmJ2KQfF-i0d5VtvFk_6tEhs6cKmsww_sKACK-w1cBzrlFdOCtCdNrgdIVciNX9DQAJ_Hs9FW-EUqFN1rx8pjXWR4PF2kIbKOQ8oJwp8tXLBHyhCSXLs1xpYW7QUzn0J6VC4-ZcO27fr7RK_XG9eUIWV6l7vD-O5Y'
    }
    logging.debug("personal_info.login_id: "+ personal_info.login_id)
    # logging.debug("personal_info.login_pwd: "+ personal_info.login_pwd)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    # response = session.get(BAEKJUN_URL + '/logout', headers=headers)
    # if response.status_code != 200:
    #     logging.debug('logout fail[' + str(response.status_code) + ']')
    #     return None

    logging.debug("before login page session cookies: " + str(session.cookies))
    logging.debug("before login page session headers: " + str(session.headers))

    response = session.get(BAEKJUN_URL + '/login?next=%2Fgroup%2Fpractice%2F20868', headers=headers)
    if response.status_code < 200 or response.status_code >= 300:
        logging.debug('Get login page fail[' + str(response.status_code) + ']')
        return None
    logging.debug('Get login page succ[' + str(response.status_code) + ']')

    logging.debug("before login session cookies: " + str(session.cookies))
    logging.debug("before login response cookies: " + str(response.cookies))
    logging.debug("before login session headers: " + str(session.headers))
    logging.debug("before login response headers: " + str(response.headers))

    response = session.post(BAEKJUN_URL + '/signin', headers=headers, data=login_data)
    if response.status_code == 200:
        logging.debug('login success')
        logging.debug("login session cookies: " + str(session.cookies))
        logging.debug("login response cookies: " + str(response.cookies))
        logging.debug("login session headers: " + str(session.headers))
        logging.debug("login response headers: " + str(response.headers))
        # logging.debug("login response body: " + str(response.text))
        return session
    else:
        logging.debug('login fail[' + str(response.status_code) + ']')
        return None

def get_solved_api_problem_level(session, problem_number):
    logging.debug('start get_solved_api_problem_level() problem_numberm: ' + str(problem_number))

    headers = {
        'Accept': 'application/json',
        'x-solvedac-language': 'ko'
    }

    response = session.get('https://solved.ac/api/v3/problem/lookup?problemIds=' + str(problem_number), headers=headers)
    api_result = response.json()

    for res in api_result:
        logging.debug('res: ' + str(res))

    level = int(api_result[0]['level'])
    logging.debug('level: ' + tier.TIER_ID_TO_STR[level])

    return level

def crawling(session):
    logging.debug('start crawling()')
    
    if session == None:
        session = requests.Session()

    msg_datas = []
    msg_data_id = 1
    soup = BeautifulSoup()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    for data in personal_info.list_of_datas:
        if data[0] == '':
            logging.debug('empty member')
            continue

        #
        # 푼 문제 수
        # 시도 횟수
        # 가장 난이도가 높은 문제
        #
        solve_problem_number = 0
        number_of_attempt = 0
        maximum_problem_level = 0

        is_done = False # 다음 페이지로 넘어갈 필요가 있는지 판단
        is_first = True
        while not is_done:
            if is_first:
                url = BAEKJUN_URL + '/status?problem_id=&user_id=' + data[personal_info.BAEKJUN_ID] + '&language_id=-1&result_id=-1'
                is_first = False
            else:
                next_page = soup.find(id='next_page').get('href')
                url = BAEKJUN_URL + next_page
            logging.debug("url: " + url)

            for i in range(RETRY_CNT):
                # response = requests.get(url, headers=headers)
                response = session.get(url, headers=headers)
                # response = requests.get(url)
                logging.debug("response.status_code: " + str(response.status_code))
                if (response.status_code == 200):
                    break
                elif (response.status_code == 202):
                    get_solved_api_problem_level(session, 11866)
                if (i + 1 == RETRY_CNT):
                    logging.debug('status page fail...')
                    return None
                logging.debug("re request!!")
            logging.debug("response.text: " + response.text)
            soup = BeautifulSoup(response.text, 'html.parser')

            logging.debug("session cookies: " + str(session.cookies))
            logging.debug("response cookies: " + str(response.cookies))
            logging.debug("session headers: " + str(session.headers))
            logging.debug("response headers: " + str(response.headers))
            # logging.debug("soup: " + str(soup.prettify()))

            # 원하는 요소 추출
            table = soup.find('table')
            rows = table.find_all('tr')

            # 첫 번째 행은 헤더이므로 건너뜁니다.
            for row in rows[1:]:
                columns = row.find_all('td')

                # 일주일 이내에 제출한 기록인지 확인
                original_time = columns[SUBMIT_TIME].find('a').get('title')
                today = datetime.today().date()
                parsed_date = datetime.strptime(original_time, '%Y-%m-%d %H:%M:%S').date()
                if (today - parsed_date).days < 1:
                    continue
                if (today - parsed_date).days > 7:
                    is_done = True
                    break

                # 시도한 횟수
                number_of_attempt += 1
                
                # 문제를 맞췄는지
                if columns[RESULT].text == '맞았습니다!!' or '점' in columns[RESULT].text:
                    # 맞은 문제 수
                    solve_problem_number += 1

                    # 가장 난이도가 높은 문제
                    logging.debug('PROBLEM_ID: ' + columns[PROBLEM_ID].find('a').text)
                    level = get_solved_api_problem_level(session, int(columns[PROBLEM_ID].find('a').text))
                    if maximum_problem_level < level:
                        maximum_problem_level = level

            ### for row in rows[1:]:
        ### while not is_done:

        # #
        # # 그룹 내 랭킹
        # # - 상위 3명
        # # - 내 랭킹
        # #
        # group_top_3 = ''
        # group_member_rank = 0

        # response = session.get(BAEKJUN_URL + '/group/practice/20868', headers=headers)
        # if response.status_code != 200:
        #     logging.debug('group page error[' + str(response.status_code) + ']')
        #     return None
        # soup = BeautifulSoup(response.text, 'html.parser')
        # # logging.debug("soup: " + str(soup))

        # # 원하는 요소 추출
        # table = soup.find('table')
        # rows = table.find_all('tr')

        # # 첫 번째 행은 헤더이므로 건너뜁니다.
        # for row in rows[1:]:
        #     columns = row.find_all('td')
        #     href = columns[PRACTICE_NAME].find('a').get('href')

        # response = session.get(BAEKJUN_URL + href, headers=headers)
        # if response.status_code != 200:
        #     logging.debug('practice page error[' + str(response.status_code) + ']')
        #     return None
        # soup = BeautifulSoup(response.text, 'html.parser')
        # # logging.debug("soup: " + str(soup))

        # # 첫 번째 행은 헤더이므로 건너뜁니다.
        # for row in rows[1:]:
        #     ths = row.find_all('th')
        #     if int(ths[GROUP_RANK].trim()) >= 1 and int(ths[GROUP_RANK].trim()) <= 3:
        #         group_top_3 += ths[BAEKJUN_ID] + ' '
        #     if ths[BAEKJUN_ID] == data[personal_info.BAEKJUN_ID]:
        #         group_member_rank = int(ths[GROUP_RANK].trim())
        # ### for row in rows[1:]:
 
        #
        # solved.ac API
        #
        headers = {
            'Accept': 'application/json',
            'x-solvedac-language': 'ko'
        }

        response = session.get('https://solved.ac/api/v3/user/show?handle=just_junyan', headers=headers)
        api_result = response.json()
        # logging.debug(data)

        # 사용자 티어
        solved_member_tier = tier.TIER_ID_TO_STR[int(api_result['tier'])]
        # logging.debug(solved_member_tier)

        # 사용자 레이팅
        solved_member_rating = int(api_result['rating'])
        # logging.debug(solved_member_rating)

        # 사용자 랭킹
        solved_member_rank = int(api_result['rank'])
        # logging.debug(solved_member_rank)

        # msg_data 채우기
        msg_data = MsgData()
        msg_data.member_baekjun_id = data[personal_info.BAEKJUN_ID]
        msg_data.member_email

        msg_data.msg_data_id = msg_data_id
        msg_data_id += 1  

        msg_data.member_name = data[personal_info.NAME]
        msg_data.member_baekjun_id = data[personal_info.BAEKJUN_ID]
        msg_data.member_phone_number = data[personal_info.PHONE_NUMBER]
        msg_data.member_email = data[personal_info.EMAIL]


        # msg_data.group_top_3 = group_top_3
        # msg_data.group_member_rank = group_member_rank

        msg_data.solve_problem_number = solve_problem_number
        msg_data.number_of_attempt = number_of_attempt

        msg_data.maximum_problem_level = tier.TIER_ID_TO_STR[maximum_problem_level]

        msg_data.solved_member_tier = solved_member_tier
        msg_data.solved_member_rating = solved_member_rating
        msg_data.solved_member_rank = solved_member_rank

        logging.debug(msg_data)
        msg_datas.append(msg_data)
    ### for data in personal_info.list_of_datas:

    return msg_datas