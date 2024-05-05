import crawling
import send_alarm

if __name__ == '__main__':
    msg_datas = crawling.crawling()
    send_alarm.send_alarm(msg_datas)