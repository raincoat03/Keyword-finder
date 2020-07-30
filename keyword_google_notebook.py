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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pynput
import pyautogui
import telepot

start = time.time()
date = datetime.today()

desktop = "C:/Users/yang/Desktop/"
main_notebook = "C:/Users/june/Desktop/"

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
credentials = ServiceAccountCredentials.from_json_keyfile_name(main_notebook + "keyword-google.json", scope)
gc = gspread.authorize(credentials)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1QYB0Qx1NfkIAGUDMdvUkXqmnXKqJnJL5mhI8XeaOh_w/edit#gid=0"

# 텔레그램 설정
token = "1317706045:AAEC0L92We9IWXzt7jqJuhuN8TpXauondYU"
host = "1382194943"
bot = telepot.Bot(token)

# 스프레스시트 문서 가져오기
doc = gc.open_by_url(spreadsheet_url)

# 시트 선택하기
worksheet = doc.get_worksheet(0)
time.sleep(10)

# google에서 필터링 되지 않은 키워드 가져오기
filter_list = worksheet.col_values(13)
filter_list = [v for v in filter_list if v]
already_list = []
time.sleep(10)

already_keyword_list = worksheet.col_values(1)
already_keyword_list = [v for v in already_keyword_list if v]
already_search_filter_list = []
for i in range(len(already_keyword_list)):
    if already_keyword_list[i] not in filter_list:
        already_search_filter_list.append(already_keyword_list[i])
already_search_filter_list = [v for v in already_search_filter_list if v]
time.sleep(10)
already_price_list = worksheet.col_values(2)
already_price_list = [v for v in already_price_list if v]
already_price_list = list(map(int, already_price_list))
time.sleep(10)
already_search_list = worksheet.col_values(3)
already_search_list = [v for v in already_search_list if v]
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

url_naver = "https://searchad.naver.com/login"
id_naver = "lyrical98"
password_naver = "dmsgur!23"
url_google = "https://ads.google.com/aw/keywordplanner/home?ocid=513665264&euid=412882241&__u=1062527609&uscid=513665264&__c=2375329136&authuser=0"
id_google = "jahab0001"
password_google = "ehgur112?!"
url_stack = "https://stackoverflow.com/users/login?ssrc=head"
id_xpath = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input"
password_xpath = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"
chromedriver = main_notebook + "chromedriver.exe"
bot.sendMessage("@navergooglekeyword", "google keyword 작업 시작")
num = 1
keyboard = pynput.keyboard.Controller()
keyboard_key = pynput.keyboard.Key
forbidden = "\!@%,*{}<>;"

while len(already_search_filter_list) != 0:
    start = time.time()
    # stackoverflow 로그인 화면
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(chromedriver, options=options)
    driver.maximize_window()
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
    temp_list = []
    keyword_input = driver.find_element_by_xpath("/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/kp-root/div/div/view-loader[2]/splash-view/div/div/div[1]/splash-cards/div/div[2]/div[3]/focus-trap/div[2]/div[1]/div/validated-text-input/div/material-input/div[1]/div[1]/div/div[2]/textarea")
    already_search_filter_list = []
    for i in range(len(already_keyword_list)):
        if (already_keyword_list[i] not in filter_list) and (already_keyword_list[i] not in already_search_list):
            already_search_filter_list.append(already_keyword_list[i])
    x = 500
    y = 500
    for j in already_search_filter_list[:499]: # 한 페이지에 500개까지만 가능
        if any(sym in j for sym in forbidden):
            continue
        else:
            keyword_input.send_keys("["+j+"]")
            keyword_input.send_keys(Keys.ENTER)
            temp_list.append([j])
            time.sleep(0.5)
            pyautogui.moveTo(x, y)
            x += 1
            y += 1
    time.sleep(2)
    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/kp-root/div/div/view-loader[2]/splash-view/div/div/div[1]/splash-cards/div/div[2]/div[3]/focus-trap/div[2]/div[1]/div/div[2]/material-button/material-ripple")))
    driver.execute_script("arguments[0].click();", element) # 시작하기 버튼
    time.sleep(10)
    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/kp-root/div/div/view-loader[2]/plan-keywords-forecasts-view/plan-view/div/div/tableview/div[6]/div/div/div/pagination-bar/div/div[2]/div[1]/material-dropdown-select/dropdown-button/div/span")))
    driver.execute_script("arguments[0].click();", element) # 한 페이지에 보이는 개수 버튼
    time.sleep(2)
    try:
        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[13]/div/div/div[2]/div/material-list/div/div/material-select-dropdown-item[6]")))
        driver.execute_script("arguments[0].click();", element)  # 개수 500개 클릭
    except:
        driver.execute_script("arguments[0].click();", element) # 개수 500개 클릭
        pass
    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/kp-root/div/div/view-loader[2]/plan-keywords-forecasts-view/plan-view/div/slider-panel/div/div[1]/div/div/summary-container/div/material-expansionpanel/div/div[1]/div/material-icon/i")))
    driver.execute_script("arguments[0].click();", element) # 그래프 나타나는 버튼
    time.sleep(5)

    # 그래프 이동
    x = 1492
    y = 483
    pyautogui.moveTo(x, y)
    pyautogui.moveTo(x, y)
    pyautogui.moveTo(x, y)
    time.sleep(5)
    pyautogui.click(x, y)
    time.sleep(5)
    pyautogui.click(x, y+15)
    time.sleep(5)
    pyautogui.click(x, y)
    time.sleep(5)
    pyautogui.click(x, y+15)
    time.sleep(5)
    pyautogui.click(x, y)
    time.sleep(5)
    pyautogui.click(x, y+15)
    time.sleep(5)


    # 키워드 및 비용 데이터 수집
    time.sleep(2)
    keyboard.press(keyboard_key.ctrl)
    keyboard.press(keyboard_key.end)
    keyboard.release(keyboard_key.end)
    keyboard.press(keyboard_key.home)
    keyboard.release(keyboard_key.home)
    keyboard.release(keyboard_key.ctrl)
    for _ in range(50):
        keyboard.press(keyboard_key.page_down)
        keyboard.release((keyboard_key.page_down))
        time.sleep(0.5)

    time.sleep(2)
    raw_data_list, keyword_list, keyword_price_list, keyword_filter_list = [], [], [], []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    raw_data = soup.select("div.particle-table-row")
    for i in raw_data:
        i = i.text.split()
        raw_data_list.append(i)
    print(len(raw_data_list))
    bot.sendMessage("@navergooglekeyword", str(len(raw_data_list)))

    for i in raw_data_list:
        name = i[0].replace("[", "").replace("]", "")
        price = i[5].replace("₩", "").replace(",", "")
        keyword_list.append([name, int(price)])

    for i in range(len(keyword_list)):
        if keyword_list[i][1] <= 30000:
            keyword_filter_list.append(keyword_list[i])

    # 추가할 위치
    location_list = worksheet.col_values(3)
    time.sleep(10)
    location_list = [v for v in location_list if v]
    location = len(location_list)
    value_for_doc = "naver!" + "C" + str(location + 1)
    doc.values_update(value_for_doc, params={'valueInputOption': 'RAW'}, body={'values': keyword_filter_list})
    time.sleep(10)
    length_for_filter_list = len(filter_list)
    value_for_filter_list = "naver!" + "M" + str(length_for_filter_list + 1)
    doc.values_update(value_for_filter_list, params={'valueInputOption': 'RAW'}, body={'values': temp_list})
    time.sleep(10)
    filter_list = worksheet.col_values(13)
    filter_list = [v for v in filter_list if v]
    driver.quit()
    time.sleep(10)
    already_search_list = worksheet.col_values(3)
    already_search_list = [v for v in already_search_list if v]
    time.sleep(10)

    # 정렬 후 재입력
    sort_list = []
    google_filter_keyword_list = worksheet.col_values(3)
    google_filter_keyword_list = [v for v in google_filter_keyword_list if v]
    time.sleep(10)
    google_filter_price_list = worksheet.col_values(4)
    google_filter_price_list = [v for v in google_filter_price_list if v]
    google_filter_price_list = list(map(int, google_filter_price_list))
    time.sleep(10)
    for i in range(len(google_filter_keyword_list)):
        sort_list.append([google_filter_keyword_list[i], google_filter_price_list[i]])
    sort_list.sort(key=lambda x: x[1])
    doc.values_update("naver!C1", params={'valueInputOption': 'RAW'}, body={'values': sort_list})
    time.sleep(10)
    google_filter_keyword_list = worksheet.col_values(3)
    google_filter_keyword_list = [v for v in google_filter_keyword_list if v]
    time.sleep(10)

    # naver 클릭수 합 넣어주기
    price_list = []
    for i in range(len(google_filter_keyword_list)):
        if google_filter_keyword_list[i] in already_keyword_list:
            a = already_keyword_list.index(google_filter_keyword_list[i])
            print(a)
            price_list.append([already_price_list[a]])
    doc.values_update("naver!E1", params={'valueInputOption': 'RAW'}, body={'values': price_list})
    print("이번 회차 완료")
    print(time.time()-start)
    bot.sendMessage("@navergooglekeyword", "google keyword 수집 완료, " + "횟수: " + str(num) + "번, " + "걸린 시간: " + str(time.time()-start))
    num += 1
