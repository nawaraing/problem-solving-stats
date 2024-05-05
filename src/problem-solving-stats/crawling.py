import personal_info
import tier

import requests
from bs4 import BeautifulSoup
from datetime import datetime

SUBMIT_ID = 0
BAEKJUN_ID = 1
PROBLEM_ID = 2
RESULT = 3
MEMORY = 4
TIME = 5
LANGUAGE = 6
CODE_LENGTH = 7
SUBMIT_TIME = 8

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
        self.member_tier = ''           # solved.ac 티어
        self.member_rating = 0          # solved.ac 래이팅
        self.member_rank = 0            # solved.ac 랭크
    
    def __str__(self):
        return f"MsgData: msg_data_id[{self.msg_data_id}] member_name[{self.member_name}] member_baekjun_id[{self.member_baekjun_id}] member_phone_number[{self.member_phone_number}] member_email[{self.member_email}] solve_problem_number[{self.solve_problem_number}] member_tier[{self.member_tier}] member_rating[{self.member_rating}] member_rank[{self.member_rank}]"

def crawling():
    msg_datas = []
    msg_data_id = 1

    for data in personal_info.list_of_datas:
        url = 'https://www.acmicpc.net/status?problem_id=&user_id=' + data[personal_info.BAEKJUN_ID] + '&language_id=-1&result_id=-1'
        print("url: " + url)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        # response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print("soup: " + str(soup))

        # 원하는 요소 추출
        table = soup.find('table')
        # print('table: ' + str(table))
        rows = table.find_all('tr')

        solve_problem_number = 0
        number_of_attempt = 0
        # 첫 번째 행은 헤더이므로 건너뜁니다.
        for row in rows[1:]:
            columns = row.find_all('td')

            # 일주일 이내에 제출한 기록인지 확인
            original_time = columns[SUBMIT_TIME].find('a').get('title')
            today = datetime.today().date()
            parsed_date = datetime.strptime(original_time, '%Y-%m-%d %H:%M:%S').date()
            if (today - parsed_date).days > 7:
                continue

            # 시도한 횟수
            number_of_attempt += 1
            
            # 맞은 문제 수
            if columns[RESULT].text == '맞았습니다!!':
                solve_problem_number += 1

        # solved.ac api
        headers = {
            'Accept': 'application/json',
            'x-solvedac-language': 'ko'
        }
        response = requests.get('https://solved.ac/api/v3/user/show?handle=just_junyan', headers=headers)
        api_result = response.json()
        # print(data)

        # 사용자 티어
        member_tier = tier.TIER_ID_TO_STR[int(api_result['tier'])]
        print(member_tier)

        # 사용자 래이팅
        member_rating = int(api_result['rating'])
        print(member_rating)

        # 사용자 랭킹
        member_rank = int(api_result['rank'])
        print(member_rank)

        # 
        msg_data = MsgData()
        msg_data.member_baekjun_id = data[personal_info.BAEKJUN_ID]
        msg_data.member_email

        msg_data.msg_data_id = msg_data_id
        msg_data_id += 1  

        msg_data.member_name = data[personal_info.NAME]
        msg_data.member_baekjun_id = data[personal_info.BAEKJUN_ID]
        msg_data.member_phone_number = data[personal_info.PHONE_NUMBER]
        msg_data.member_email = data[personal_info.EMAIL]

        msg_data.solve_problem_number = solve_problem_number
        msg_data.number_of_attempt = number_of_attempt
        msg_data.member_tier = member_tier
        msg_data.member_rating = member_rating
        msg_data.member_rank = member_rank

        # print(msg_data)
        msg_datas.append(msg_data)
    return msg_datas