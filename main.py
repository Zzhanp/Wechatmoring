from time import time, localtime
import cityinfo
from requests import get, post
from datetime import datetime, date
import sys
import os
import requests
import http.client, urllib
import json
import sys
import json
import requests
import urllib.request


def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token


def get_weather(province, city):
    # 城市id
    try:
        city_id = cityinfo.cityInfo[province][city]["AREAID"]
    except KeyError:
        print("推送消息失败，请检查省份或城市是否正确")
        os.system("pause")
        sys.exit(1)
    # city_id = 101280101
    # 毫秒级时间戳
    t = (int(round(time() * 1000)))
    headers = {
      "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    response_json = eval(response_data)
    # print(response_json)
    weatherinfo = response_json["weatherinfo"]
    # 天气
    weather = weatherinfo["weather"]
    # 最高气温
    temp = weatherinfo["temp"]
    # 最低气温
    tempn = weatherinfo["tempn"]
    return weather, temp, tempn

#经典台词
def taici():
    url = 'http://api.tianapi.com/dialogue/index?key=445a76a6665922e0ea902e7b2ef88f47'
    for i in range(2):
        res = requests.get(url)
    content = res.json()
    note_en = content['newslist'][0]['dialogue']
    note_ch = content['newslist'][0]['english']
    return note_ch, note_en

#彩虹屁
def caihongpi():
    url = 'http://api.tianapi.com/caihongpi/index?key=445a76a6665922e0ea902e7b2ef88f47'
    for i in range(2):
        res = requests.get(url)
    content = res.json()
    note_en2 = content['newslist'][0]['content']
    return note_en2

#早安心语
def zaoan():
    url = 'http://api.tianapi.com/zaoan/index?key=445a76a6665922e0ea902e7b2ef88f47'
    for i in range(2):
        res = requests.get(url)
    content = res.json()
    note_en3 = content['newslist'][0]['content']
    return note_en3

#健康提示
def tishi():
    url = 'http://api.tianapi.com/healthtip/index?key=445a76a6665922e0ea902e7b2ef88f47'
    for i in range(2):
        res = requests.get(url)
    content = res.json()
    note_en4 = content['newslist'][0]['content']
    return note_en4

def send_message(to_user, access_token, city_name, weather, max_temperature, min_temperature, note_en2, note_en3):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取生日的月和日
    birthday_month = int(config["birthday"].split("-")[1])
    birthday_day = int(config["birthday"].split("-")[2])
    # 今年生日
    year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    # 获取纪念日的月和日
    anniversary_month = int(config["anniversary"].split("-")[1])
    anniversary_day = int(config["anniversary"].split("-")[2])
    # 今年纪念日
    anniversary_year_date = date(year, anniversary_month, anniversary_day)
    if today > anniversary_year_date:
        anniversary_date = date((year + 1), anniversary_month, anniversary_day)
        anniver_day = str(anniversary_date.__sub__(today)).split(" ")[0]
    elif today == anniversary_year_date:
        anniver_day = 0
    else:
        anniversary_date = anniversary_year_date
        anniver_day = str(anniversary_date.__sub__(today)).split(" ")[0]
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": "#00FFFF"
            },
            "city": {
                "value": city_name,
                "color": "#808A87"
            },
            "weather": {
                "value": weather,
                "color": "#ED9121"
            },
            "min_temperature": {
                "value": min_temperature,
                "color": "#00FF00"
            },
            "max_temperature": {
                "value": max_temperature,
                "color": "#FF6100"
            },
            "love_day": {
                "value": love_days,
                "color": "#87CEEB"
            },
            "birthday": {
                "value": birth_day,
                "color": "#FF8000"
            },
            "anniversary": {
                "value": anniver_day,
                "color": "#EE82EE"
            },
            # "note_en": {
            #     "value": note_en,
            #     "color": "#EE82EE"
            # },
            # "note_ch": {
            #     "value": note_ch,
            #     "color": "#EE82EE"
            # },
            "note_en2": {
                "value": note_en2,
                "color": "#A8FF00"
            },
            "note_en3": {
                "value": note_en3,
                "color": "#00ADFF"
            }
        }
    }
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)

    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 传入省份和市获取天气信息
    province, city = config["province"], config["city"]
    weather, max_temperature, min_temperature = get_weather(province, city)

    # 彩虹屁
    note_en2 = caihongpi()
    # 早安
    note_en3 = zaoan()
    # 公众号推送消息
    for user in users:
        send_message(user, accessToken, city, weather, max_temperature, min_temperature, note_en2, note_en3)
    os.system("pause")