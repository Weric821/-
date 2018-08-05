# !/usr/bin/python
# -*- coding: utf-8 -*-

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

from bs4 import BeautifulSoup
import requests

import jieba.posseg as pseg

import multiprocessing as mp
import threading
import time

my_bot = ChatBot("Bot")
'''
my_bot.train([
                    "請幫我尋找",
                    "好哇！"
            ])
my_bot.train([
                    "幫我找找",
                    "遵命，我的主人~"
            ])
my_bot.train([
                    "請問什麼是",
                    "我找找看喔！"
            ])
'''
global_dict = {'Time' : "0"}
dict={}
def get_stdtime():
    while(1):
        time_res = requests.get('http://www.stdtime.gov.tw/chinese/home.aspx' )
        soup = BeautifulSoup(time_res.content, 'html.parser')
        stdtime=soup.find('span',id='TimeTag')
        for word in stdtime:
            stdtime_substr=word
        global_dict['Time'] = str(stdtime_substr)
        #print(stdtime_substr)
        for dict_job, dict_time in dict.items():
            if (dict_time <= str(global_dict['Time'])):
                print("Robot: 提醒您！" + dict_job + " " + dict_time)
                del dict[dict_job]
                break;
        time.sleep(15)

def chatbot_func():

    while(1):

        s = input()
        output = my_bot.get_response(s)

        if(s=='工作提醒'):
            job_work =input("Robot: 提醒您什麼事呢?  ")
            job_time = input("Robot: 什麼時候要提醒您呢?  ")
            dict[job_work]=job_time
        elif(s=='現在時間'):
            print("Robot: "+global_dict['Time'])
        else:
            print("Robot:", output)

            # 斷詞處理
            if (output == "好哇！" or output == "遵命，我的主人~" or output == "我找找看喔！"):
                words = pseg.cut(s)
                ss = str();

                control = 0;  # 記詞性長度
                control2 = 0;  # 記是否有'n'在詞性中

                for word, flag in words:
                    for i in range(len(flag)):
                        if (flag[i] == 'n'):
                            control += 1;
                            ss = ss + word
                        else:
                            if (control >= 1):
                                control2 = 1;
                            break;
                    if (control >= 1 and control2 == 1):
                        break;

                # 爬蟲
                res = requests.get('https://zh.wikipedia.org/wiki/' + ss)
                soup = BeautifulSoup(res.content, 'html.parser')

                ss2 = str(soup.p)  # soup.p代表第一段<p>標籤

                count = int(1)
                flag = int(1)
                for word in ss2:
                    for word2 in word:
                        if (word2 == '<' or word2 == '['):
                            flag = 0
                        elif (word2 == '>' or word2 == ']'):
                            flag = 1
                        elif (flag == 1):
                            if (count % 60 != 0):
                                print(word2, end="")
                                count += 1
                            else:
                                print(word2)
                                count += 1
                if (count == 1):
                    print("查不到相關資料餒！", end="")
                print()

def main():
    t = threading.Thread(target=chatbot_func)
    t.start()
    t2 = threading.Thread(target=get_stdtime)
    t2.start()

if __name__ == '__main__':
    main()