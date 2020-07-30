from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import pynput
import pyautogui
import openpyxl
from openpyxl import load_workbook
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import pynput
import pyautogui
import telepot

# 텔레그램 설정
token = "1317706045:AAEC0L92We9IWXzt7jqJuhuN8TpXauondYU"
host = "1382194943"
bot = telepot.Bot(token)

start = time.time()
# Naver Keyword 전체 조사
bot.sendMessage("@navergooglekeyword", "Naver Keyword 전체 조사 시작")
exec(open("keyword_naver_notebook_first.py", encoding="UTF-8").read())
bot.sendMessage("@navergooglekeyword", "Naver Keyword 전체 조사 완료")
time.sleep(10)

# Google Filtering
bot.sendMessage("@navergooglekeyword", "Google Filtering 작업 시작")
exec(open("keyword_google_notebook.py", encoding="UTF-8").read())
bot.sendMessage("@navergooglekeyword", "Google Filtering 작업 완료")
time.sleep(10)

# Naver에서 나머지 정보 수집
bot.sendMessage("@navergooglekeyword", "Naver에서 나머지 정보 수집 시작")
exec(open("keyword_naver_notebook.py", encoding="UTF-8").read())
bot.sendMessage("@navergooglekeyword", "Naver에서 나머지 정보 수집 작업 완료")
bot.sendMessage("@navergooglekeyword", "전체 작업 종료. " + "소요 시간은 " + str(start-time.time()))
time.sleep(10)