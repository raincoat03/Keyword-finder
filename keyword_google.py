from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import openpyxl
from openpyxl import load_workbook
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
start = time.time()
date = datetime.today()

chromedriver = "C:/Users/june/Desktop/chromedriver.exe"
options = webdriver.ChromeOptions()

'''
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('window-size=1920x1080')
options.add_argument('lang=ko_KR')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
'''
scope = [
"https://spreadsheets.google.com/feeds",
"https://www.googleapis.com/auth/drive",
]
json_file_name = "keyword-google"
credentials = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/june/Desktop/keyword-google.json", scope)
gc = gspread.authorize(credentials)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1QYB0Qx1NfkIAGUDMdvUkXqmnXKqJnJL5mhI8XeaOh_w/edit#gid=0"

# 스프레스시트 문서 가져오기
doc = gc.open_by_url(spreadsheet_url)

# 시트 선택하기
worksheet = doc.get_worksheet(0)

# google에서 필터링 되지 않은 키워드 가져오기
already_list = []
already_keyword_list = worksheet.col_values(1)
already_keyword_list = [v for v in already_keyword_list if v]
time.sleep(10)
already_price_list = worksheet.col_values(2)
already_price_list = [v for v in already_price_list if v]
already_price_list = list(map(int, already_price_list))
time.sleep(10)
already_expect_click_list = worksheet.col_values(3)
already_expect_click_list_list = [v for v in already_expect_click_list if v]
time.sleep(10)
already_bid_price_list = worksheet.col_values(4)
already_bid_price_list = [v for v in already_bid_price_list if v]
time.sleep(10)
already_expect_cost_list = worksheet.col_values(5)
already_expect_cost_list = [v for v in already_expect_cost_list if v]
x = len(already_keyword_list)
m = len(already_expect_cost_list)

for i in range(m, x):
    already_list.append([already_keyword_list[i], already_price_list[i]])

google = 1
if google == 1:
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    import pyautogui
    driver = webdriver.Chrome(chromedriver, options = options)
    driver.maximize_window()
    url_naver = "https://searchad.naver.com/login"
    id_naver = "lyrical98"
    password_naver = "dmsgur!23"
    url_google = "https://ads.google.com/aw/keywordplanner/home?ocid=513665264&euid=412882241&__u=1062527609&uscid=513665264&__c=2375329136&authuser=0"
    id_google = "jahab0001"
    password_google = "ehgur112?!"
    url_stack = "https://stackoverflow.com/users/login?ssrc=head"
    id_xpath = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input"
    password_xpath = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"

    # stackoverflow 로그인 화면
    driver.get(url_stack)
    time.sleep(2)
    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div[2]/button[1]")))
    driver.execute_script("arguments[0].click();", element)
    time.sleep(2)
    google_id_login = driver.find_element_by_xpath(id_xpath)
    google_id_login.send_keys(id_google)
    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='identifierNext']/div/button/div[2]")))
    driver.execute_script("arguments[0].click();", element)
    time.sleep(5)
    google_password_login = driver.find_element_by_xpath(password_xpath)
    time.sleep(2)
    google_password_login.send_keys(password_google)
    time.sleep(2)
    google_password_login.send_keys(Keys.ENTER)

    # google ads 이동
    time.sleep(5)
    driver.get(url_google)
    time.sleep(10)
    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]/div")))
    driver.execute_script("arguments[0].click();", element) # Ads 로그인을 위한 계정 클릭
    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/kp-root/div/div/view-loader[2]/splash-view/div/div/div[1]/splash-cards/div/div[2]/div[3]/div/span")))
    driver.execute_script("arguments[0].click();", element)
    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/kp-root/div/div/view-loader[2]/splash-view/div/div/div[1]/splash-cards/div/div[2]/div[3]/focus-trap/div[2]/div[1]/div/validated-text-input/div/material-input/div[1]/div[1]/div/div[2]/textarea")))
    driver.execute_script("arguments[0].click();", element)
    time.sleep(1)

    # keyword 입력
    keyword_input = driver.find_element_by_xpath("/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/kp-root/div/div/view-loader[2]/splash-view/div/div/div[1]/splash-cards/div/div[2]/div[3]/focus-trap/div[2]/div[1]/div/validated-text-input/div/material-input/div[1]/div[1]/div/div[2]/textarea")
    for i in range(500): # 한 페이지에 500개까지만 가능
        keyword_input.send_keys("["+already_list[i][0]+"]")
        keyword_input.send_keys(Keys.ENTER)
        time.sleep(0.5)
    time.sleep(2)
    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/kp-root/div/div/view-loader[2]/splash-view/div/div/div[1]/splash-cards/div/div[2]/div[3]/focus-trap/div[2]/div[1]/div/div[2]/material-button/material-ripple")))
    driver.execute_script("arguments[0].click();", element) # 시작하기 버튼
    time.sleep(10)
    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/kp-root/div/div/view-loader[2]/plan-keywords-forecasts-view/plan-view/div/div/tableview/div[6]/div/div/div/pagination-bar/div/div[2]/div[1]/material-dropdown-select/dropdown-button/div/span")))
    driver.execute_script("arguments[0].click();", element) # 한 페이지에 보이는 개수 버튼
    time.sleep(3)
    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[14]/div/div/div[2]/div/material-list/div/div/material-select-dropdown-item[6]")))
    driver.execute_script("arguments[0].click();", element) # 개수 500개 클릭
    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/kp-root/div/div/view-loader[2]/plan-keywords-forecasts-view/plan-view/div/slider-panel/div/div[1]/div/div/summary-container/div/material-expansionpanel/div/div[1]/div/material-icon/i")))
    driver.execute_script("arguments[0].click();", element) # 그래프 나타나는 버튼
    time.sleep(5)

    # 그래프 이동
    x = 1491
    y = 457
    pyautogui.moveTo(x, y)
    pyautogui.moveTo(x, y)
    pyautogui.moveTo(x, y)
    time.sleep(5)
    pyautogui.click(x, y)
    time.sleep(10)
    pyautogui.click(x, y)
    time.sleep(10)
    pyautogui.click(x, y)
    time.sleep(10)

    print("성공")
   # 키워드 및 비용 데이터 수집