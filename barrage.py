import requests
import random
import time
import sys
import re

av_code = 'the av code that you want to send'            # 发送的av号

################################################
#              需要修改的值在这里               #
#        这三个值通过自己发一次弹幕抓包获取       #
#             注意这三个值容易变更              #
################################################

# 你的rnd
rnd = 'your_rnd'

# 你的csrf
# 这个csrf有比较长的时效
csrf = 'your_csrf'

# 你的cookie， 以下算是一个cookie池，你可以自己多次采集多个cookie来用
# mark1: 当你每隔5s（隔10+s和5s是一样的）发一条弹幕达15条之后，b站需要你等待300s
# mark2: 当出现mark1时， 你手动再去b站发一条弹幕，b站会给你重新分配一个cookie
# mark3: 新的cookie的包里的rnd是变了的，但却还能成功发弹幕， 神奇
# mark4: b站cookie时效大概一小时或者半小时
cookie = ['cookie1', 'cookie2', 'cookie3']


################################################

session = requests.Session()
base_url = 'https://interface.bilibili.com/dmpost?cid={cid}&aid={av_code}&pid=1&ct=1'
data = {
    'pool': '0',
    'mode': '1',

    'message': '',                             # 弹幕的内容
    'playTime': '0',                           # 弹幕的发送所在的进度条时间, 以秒为基准,可带小数
    'fontsize': '25',                          # 弹幕字体大小
    'color': '16777215',                       # 弹幕字体颜色
    'date': '2018-02-23 20:17:59',             # 弹幕发送的时间

    'rnd': rnd,
    'cid': '',
    'csrf': csrf                               # 你的csrf
}
headers = {
    'Cookie': cookie[0],
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}
pattern = re.compile(r'cid=(.+?)&')


def get_cid(av_code):
    url = 'https://www.bilibili.com/video/av{av_code}/'.format(av_code=av_code)
    try:
        text = session.get(url=url, timeout=2).text
        cid = pattern.findall(text)[0]
    except:
        cid = ''
    return cid

cid = ''


def send_barrage(message, av_code='', play_time='0', font_size='25', color='ffffff'):
    if type(av_code) != type(str):
        av_code = str(av_code)
    global cid
    if cid == '':
        # 第一次获取的话,cid是'' 空值，需要获取
        cid = get_cid(av_code)

        if cid == '':
            # 若获取后cid仍为空值，失败，返回
            print('发送失败', 'cid获取失败')
            return -1

    url = base_url.format(cid=cid, av_code=av_code)
    data['message'] = message               # 弹幕内容
    data['playTime'] = play_time            # 弹幕所在的时间戳
    data['fontsize'] = font_size            # 弹幕字体大小
    data['color'] = str(int(color, 16))                   # 弹幕字体颜色
    data['date'] = time.strftime('%F %X')   # 设置弹幕发送的时间
    data['cid'] = cid

    result = eval(session.post(url=url, data=data,
                               headers=headers).text).get('message', '')
    if result == '':
        print('发送成功')
        return 0
    else:
        print('发送失败', result)
        return -1


if __name__ == '__main__':
    send_barrage(message='hello world', av_code=av_code)
