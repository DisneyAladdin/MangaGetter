#coding: utf-8
# Created by Mizuki.K and Shuto.K on 2019/10/30.
# Copyright © 2019 All rights reserved.


# ***スペック***
# ターゲット: 無料のマンガおよびチケットを使用すれば購読可能なマンガ
# チケットの回復時刻: 8:00および20:00
# 一度に使用可能なチケット枚数: 4枚
# チケットを使用して購読できる時間は12時間

PURPLE  = '\033[35m'
RED     = '\033[31m'
CYAN    = '\033[36m'
OKBLUE  = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL    = '\033[91m'
ENDC    = '\033[0m'
UNDERLINE = '\033[4m'

from time import sleep
import sys
import random
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

LOGIN_ID = 'lovedisneyaladdin@yahoo.co.jp'
LOGIN_PASSWORD = 'shuto0723'
LOGIN_URL = 'https://manga-zero.com/login'
TARGET_URL = 'https://manga-zero.com/product/3769'

# コード実行時刻の設定（チケット回復時間の15分後に設定）
RECOVERTIME1 = '08:15'
RECOVERTIME2 = '20:15'
cnt = 0

# ログインおよびチケットの取得
def login():
    b.get(LOGIN_URL)
    b.find_element_by_class_name('register-facebook').click()
    sleep(4)
    
    try:
        b.find_element_by_id('email').send_keys(LOGIN_ID)
        b.find_element_by_id('pass').send_keys(LOGIN_PASSWORD)
        b.find_element_by_id('loginbutton').click()
    except:
        print("Login directly!!")
    
    try:
        b.find_element_by_class_name('button--white.button--radius-4.button--40').click()
    except:
        print('No more getable tickets')


# チケットを使わない無料マンガの取得
def getFree():
    b.get(TARGET_URL)
    sleep(2) 
    b.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 無料で購読できるチケット数
    numBlueTicket = len(b.find_elements_by_class_name('chip-icon.chip-icon--blue'))

    for a in range(numBlueTicket):
        # エピソードを開く
        b.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        b.find_elements_by_class_name('chip-icon.chip-icon--blue')[a].click()
        print('Now loading episode ---- '+ str(a+1))
        sleep(2)
        b.find_element_by_class_name('button-direction.button-direction__horizontal').click()
        sleep(3)
        
        # ページ数の取得
        images = b.find_elements_by_class_name('canvas-wrapper')
        
        # ページの保存
        for c in range(len(images)):
            png = b.find_element_by_class_name('viewer-horizontal').screenshot_as_png
            file_name = str(a+1)+'_'+ str(c+1)+'.png'
            with open('./image/'+ file_name, 'wb') as f:
                f.write(png)
            b.find_element_by_class_name('arrow.arrow-left').click()
            sleep(3)

        # エピソードを閉じる
        b.find_element_by_class_name('button--white.button--radius-4.button--40').click()
        sleep(2)
        b.find_elements_by_class_name('button-close')[1].click()
        sleep(4)

    cnt = numBlueTicket
    return cnt

# チケットが必要なマンガの取得
def getManga():    
    b.get(TARGET_URL)
    sleep(3)
    b.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    numGreenTicket = len(b.find_elements_by_class_name('chip-icon.chip-icon--green'))

    # 一度に使用できるチケットは４枚まで
    if numGreenTicket > 4:
        numGreenTicket = 4
    
    # チケットの数だけエピソードを回す
    for x in range(numGreenTicket):
        b.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            # チケット使用可能なエピソードのうちの最初のエピソードをオープン
            b.find_elements_by_class_name('chip-icon.chip-icon--green')
            b.find_elements_by_class_name('chip-icon.chip-icon--green')[0].click()
        except:
            try:
                # チケット使用可能なエピソードが次のページにある場合，次のページへ遷移後，最初のエピソードをオープン
                b.find_element_by_class_name('next.item-pagination').click()
                sleep(3)
                b.find_elements_by_class_name('chip-icon.chip-icon--green')[0].click()
            except:
                # チケット使用可能なマンガがない場合（既に全てのマンガを購読済みの場合）
                print('manga completedly saved!')
        
        print('Now loading episode ---- '+ str(cnt+x+1))
        sleep(3) 
        b.find_element_by_class_name('button-content').click()
        sleep(3)
        b.find_element_by_class_name('button-direction.button-direction__horizontal').click()
        sleep(3)

        # ページ数の取得
        images = b.find_elements_by_class_name('canvas-wrapper')
        
        for y in range(len(images)):
            png = b.find_element_by_class_name('viewer-horizontal').screenshot_as_png
            file_name = str(cnt+x+1) + '_' + str(y+1)+'.png'
            with open('./image/'+ file_name, 'wb') as f:
                f.write(png)
            b.find_element_by_class_name('arrow.arrow-left').click()
            sleep(3)

    # エピソードを閉じる
    sleep(3)
    b.find_element_by_class_name('button--white.button--radius-4.button--40').click()
    sleep(2)
    b.find_elements_by_class_name('button-close')[1].click()
    sleep(4)



# ログファイルの読み込み
def readLogFile():
    logFile = open('log.csv','r+')
    manga_list = []
    for row in logFile:
        LINE = row.rstrip().split(',')
        ID = LINE[0]
        title = LINE[1]
        manga_list.append(title)
    logFile.close()
    return manga_list

# 欲しいマンガのリスト
def hosii():
    z = open('hosii.txt','r')
    hosii_list=[]
    for row in z:
        manga = row.rstrip()
        hosii_list.append(manga)
    return hosii_list

# 現在時刻の取得と実行するかどうかの判定
def getTime():
    dt_now = datetime.datetime.now()
    dt_h = dt_now.strftime('%H')
    dt_m = dt_now.strftime('%M')
    h_m  = str(dt_h + ':' + dt_m)
    if h_m == RECOVERTIME1 or h_m == RECOVERTIME2:
        return True
    else:
        return False

# ログを残す
def log():
    logFile = open('log.csv','a')
    episodeName = b.find_element_by_class_name('item-episode-title').text.replace('\n','').replace('無料','')
    mangaName   = b.find_element_by_class_name('product-title').text
    log_text    = mangaName+','+episodeName+'\n'
    logFile.write(log_text)
    logFile.close()

# 既に取得済みのエピソードかをチェック
def isAlreadyHave(episodeTitle):
    if episodeTitle in manga_list:
        return False
    else:
        return True


        

# Main部分（各関数を呼び出す．まだ未完成部分）
b = webdriver.Chrome('./chromedriver')
login()
sleep(2)
#hosii_list = hosii()
manga_list = readLogFile()
#log_list = readLogFile()
isTimeOk = getTime()
getFree()
getManga()
b.close()
