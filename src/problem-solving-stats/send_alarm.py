import json
import logging

import sys
sys.path.append(r'/home/runner/work/problem-solving-stats/problem-solving-stats/src/lib')
sys.path.append(r'/Users/kangjunhyeon/problem-solving-stats/src/lib')

import message
import personal_info

def send_alarm(msg_datas):
    messages = []
    for data in msg_datas:
        messages.append({
                'to': data.member_phone_number,
                'from': '01050929241',
                'subject': data.member_name + '님의 성장 기록!',
                'text': '=== History(지난 주) ===\n'
                        + '- 푼 문제 수: ' + str(data.solve_problem_number) + '문제\n'
                        + '- 시도 횟수: ' + str(data.number_of_attempt) + '회\n'
                        + '- 가장 어려운 문제: ' + str(data.maximum_problem_level) + '\n\n'

                        + '==== My Status ====\n'
                        + '- solved.ac 티어: ' + data.solved_member_tier + '\n'
                        + '- solved.ac 레이팅: ' + str(data.solved_member_rating) + '점\n'
                        + '- solved.ac 랭크: ' + str(data.solved_member_rank) + '등'
        })
    data = {
        'messages': messages
    }
    res = message.send_many(data)
    logging.debug(json.dumps(res.json(), indent=2, ensure_ascii=False))
