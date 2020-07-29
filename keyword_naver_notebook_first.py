from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import telepot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pynput
import pyautogui

desktop = "C:/Users/yang/Desktop/"
main_notebook = "C:/Users/june/Desktop/"
now = datetime.now()
date = now.strftime('%Y-%m-%d %H:%M:%S')
chromedriver = main_notebook + "chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('window-size=1920x1080')
options.add_argument('lang=ko_KR')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
driver = webdriver.Chrome(chromedriver, options=options)
url_naver = "https://searchad.naver.com/login"
id_naver = "lyrical98"
password_naver = "dmsgur!23"
search_total = []
naver_total = []
search_keyword_list = []
already_list = []
r = 1
# switch는 추가된 keyword 수집하기 위한 변수로, 1로 바꾸면 새로운 키워드 수집. 하루에 한 번만 바꿔줘도 됨
# switch == 0 : google에서 필터링 된 값으로 나머지 정보 찾기
# switch == 1 and new == 0 : naver keyword 전체 수집
# switch == 1 and new == 1 : 새로운 naver 키워드와 클릭수 합 가져오기
switch = 0
new = 0
new_keyword_number = 0

# 텔레그램 설정
token = "1317706045:AAEC0L92We9IWXzt7jqJuhuN8TpXauondYU"
host = "1382194943"
bot = telepot.Bot(token)

scope = [
"https://spreadsheets.google.com/feeds",
"https://www.googleapis.com/auth/drive",
]

json_file_name = "keyword-google"
credentials = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/june/Desktop/keyword-google.json", scope)
gc = gspread.authorize(credentials)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1QYB0Qx1NfkIAGUDMdvUkXqmnXKqJnJL5mhI8XeaOh_w/edit#gid=0"

# try:
# 문서 불러오기
doc = gc.open_by_url(spreadsheet_url)
# naver 시트 불러오기
worksheet = doc.get_worksheet(0)
# sheet header 생성
'''
worksheet.update_acell("B1", "Keyword")
time.sleep(10)
worksheet.update_acell("C1", "M+PC 클릭수")
time.sleep(10)
worksheet.update_acell("D1", "예상 클릭수")
time.sleep(10)
worksheet.update_acell("E1", "입찰가")
time.sleep(10)
worksheet.update_acell("F1", "예상비용")
time.sleep(10)
'''
# 수집한 키워드 읽기
bot.sendMessage("@navergooglekeyword", "작업 시작")
already_total_keyword_list = worksheet.col_values(1)
already_total_keyword_list = [v for v in already_total_keyword_list if v]
time.sleep(10)
already_total_price_list = worksheet.col_values(2)
already_total_price_list = [v for v in already_total_price_list if v]
time.sleep(10)
already_keyword_list = worksheet.col_values(3)
already_keyword_list = [v for v in already_keyword_list if v]
time.sleep(10)
already_google_price_list = worksheet.col_values(4)
already_google_price_list = [v for v in already_google_price_list if v]
time.sleep(10)
already_price_list = worksheet.col_values(5)
already_price_list = [v for v in already_price_list if v]
time.sleep(10)
already_expect_click_list = worksheet.col_values(6)
already_expect_click_list_list = [v for v in already_expect_click_list if v]
time.sleep(10)
already_bid_price_list = worksheet.col_values(7)
already_bid_price_list = [v for v in already_bid_price_list if v]
time.sleep(10)
already_expect_cost_list = worksheet.col_values(8)
already_expect_cost_list = [v for v in already_expect_cost_list if v]
x = len(already_keyword_list)
m = len(already_expect_cost_list)
already_price_list = list(map(int, already_price_list))
already_total_price_list = list(map(int, already_total_price_list))
print("수집한 키워드 읽기 작업 완료")
bot.sendMessage("@navergooglekeyword", "수집한 키워드 읽기 작업 완료")

for i in range(m, x):
    already_list.append([already_keyword_list[i], already_price_list[i]])
driver.get(url_naver)
id_xpath = "/html/body/marvel-root/login/div/div/div/div/fieldset/dl/dd[1]/input"
password_xpath = "/html/body/marvel-root/login/div/div/div/div/fieldset/dl/dd[2]/input"
naver_id_login = driver.find_element_by_xpath(id_xpath)
naver_id_login.send_keys(id_naver)
naver_password_login = driver.find_element_by_xpath(password_xpath)
naver_password_login.send_keys(password_naver)
naver_login_button_xpath = "/html/body/marvel-root/login/div/div/div/div/fieldset/div/span/button"
driver.find_element_by_xpath(naver_login_button_xpath).click()
time.sleep(2)

main = driver.window_handles
for handle in main:
    if handle != main[0]:
        driver.switch_to.window(handle)
        driver.close()
driver.switch_to.window(driver.window_handles[0])
naver_class_n = ""
keyword_naver_url = "https://manage.searchad.naver.com/customers/1948785/tool/keyword-planner?keywords="

# 목록 수집
## 리스트 순회
if switch == 1:
    print("목록 수집")
    bot.sendMessage("@navergooglekeyword", "목록 수집")
    for i in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22]: #
        time.sleep(1)
        driver.get("https://manage.searchad.naver.com/customers/1948785/tool/keyword-planner?keywords=")
        naver_class_check_url = "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/label/div/ul/li/i"
        time.sleep(1)
        element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/label/div/ul/li/i")))
        driver.execute_script("arguments[0].click();", element)
        enter_button = "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[3]/button"
        time.sleep(1)
        naver_class_n = str(i)
        naver_class_1 = "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/div/li["
        naver_class_2 = naver_class_n
        naver_class_3 = "]/div"  # 3 ~ 22
        click_find = naver_class_1 + naver_class_2 + naver_class_3
        time.sleep(2)
        # 목록 선택
        element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/button/i")))
        driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
        # 목록 중 가정 등 선택
        element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/div/li[" + naver_class_n + "]/div")))
        try:
            driver.execute_script("arguments[0].click();", element)
        except:
            driver.execute_script("arguments[0].click();", element)
            pass
        time.sleep(1)
        element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[3]/button")))
        driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
        ## 검색어 추출
        for j in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]: #
            search_name_list, search_pc_list, search_mobile_list = [], [], []
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            search_name = soup.select("tr > td > elena-keyword > span")
            for i in search_name:
                i = i.text.strip()
                if i[-1] == "S":
                    i.rstrip("S")
                search_name_list.append(i)
                if "일부노출" in search_name_list:
                    search_name_list.remove("일부노출")
                if "S" in search_name_list:
                    search_name_list.remove("S")
                if "19" in search_name_list:
                    search_name_list.remove("19")

            search_click_pc = soup.select("td.elenaColumn-monthlyAvePcClkCnt")
            for k in search_click_pc:
                k = k.text.strip()
                k = k.replace(",","")
                search_pc_list.append(k)

            search_click_mobile = soup.select("td.elenaColumn-monthlyAveMobileClkCnt")
            for l in search_click_mobile:
                l = l.text.strip()
                l = l.replace(",","")
                search_mobile_list.append(l)

            for i in range(len(search_name_list)):
                sum = int(round(float(search_pc_list[i]),-1))+int(round(float(search_mobile_list[i]),-1))
                temp = [search_name_list[i], sum]
                search_total.append(temp)

            next_page_1 = "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[2]/div[3]/elena-table/elena-table-paginator/div/div/nav/ul/li["
            next_page_2 = str(j)
            next_page_3 = "]/a"
            next_page = next_page_1 + next_page_2 + next_page_3
            time.sleep(1)
            driver.find_element_by_xpath(next_page).click()
            time.sleep(1)
    print("목록수집완료")
    bot.sendMessage("@navergooglekeyword", "목록수집완료")
    search_total.sort(key=lambda x:-x[1])  # 클릭수 높은 순서대로 정렬(-1), 낮은 순서대로 정렬(1)

    # already sheet 입력
    '''
    for i in range(len(search_total)):
        if i not in already_keyword_list:
            worksheet.append_row(search_total[i])
            time.sleep(10)
    print("already sheet 입력 완료")
    '''
    if switch == 1 and new == 0:
        doc.values_update("naver!A1", params={'valueInputOption': 'RAW'}, body={'values': search_total})
        bot.sendMessage("@navergooglekeyword", "1차 Keyword 수집 완료")
        print("1차 키워드 수집 완료")
        driver.close()

    elif switch == 1 and new == 1:
        new_keyword = 0
        for i in range(len(search_total)):
            if search_total[i][0] not in already_keyword_list:
                worksheet.append_row(search_total[i])
                time.sleep(10)
                new_keyword += 1
        new_keyword_number = str(new_keyword)
        bot.sendMessage("@navergooglekeyword", "새롭게 추가된 Keyword 숫자 : " + new_keyword_number)

    '''
    # 입찰가 등을 찾기 위한 목록 입력
    for i in range(len(search_total)):
        print("입찰가 등 정보 수집 시작")
        bot.sendMessage("@navergooglekeyword", "입찰가 등 정보 수집")
        if search_total[i][0] not in already_keyword_list:
            driver.get(keyword_naver_url)
            time.sleep(1)
            keyword_enter_sheet = "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[2]/div/div/form/div[1]/textarea"
            element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[2]/div/div/form/div[1]/textarea")))
            driver.execute_script("arguments[0].click();", element)
            keyword_enter = driver.find_element_by_xpath(keyword_enter_sheet)
            time.sleep(1)
            keyword_enter.send_keys(search_total[i][0])
            time.sleep(1)
            element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[2]/div/div/form/div[2]/button[2]")))
            driver.execute_script("arguments[0].click();", element)
            time.sleep(2)
            bid_price = driver.find_element_by_xpath("/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-estimate/div[3]/div[2]/div/div[1]/div[1]/div/elena-input-amt/div/input")
            start = time.time()
            for j in range(70, 100001, 50):
                time.sleep(1)
                element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-estimate/div[3]/div[2]/div/div[1]/div[1]/div/elena-input-amt/div/input")))
                driver.execute_script("arguments[0].click();", element)
                n = j
                bid_price.clear()
                bid_price.send_keys(n)
                driver.find_element_by_xpath("/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-estimate/div[3]/div[2]/div/div[1]/div[4]/button").click()
                time.sleep(2)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                click = soup.select("td.elenaColumn-clicks")
                cost = soup.select("td.elenaColumn-cost")
                cost_list = []
                for j in click:
                    j = j.text.strip()
                    j = j.replace(",", "")
                    j = int(j)
                    expect_click = j
                for k in cost:
                    k = k.text.strip()
                    k = k.strip("원")
                    k = k.replace(",", "")
                    k = k.strip()
                    k = int(k)
                    cost_list.append(k)
                print(j)
                if j >= search_total[i][1] + 30:
                    date = now.strftime('%Y-%m-%d %H:%M:%S')
                    naver_total.append([search_total[i][0],search_total[i][1],j,n,cost_list[0], date])
                    break
                time.sleep(1)
        if len(naver_total) % 10 == 0 and len(naver_total) != 0:
            for i in range(len(naver_total)):
                if i not in already_keyword_list:
                    worksheet.append_row(naver_total[i])
                    time.sleep(10)
                    print(r, time.time()-start)
                    time_config = str(time.time()-start)
                    keyword_number = str(r)
                    bot.sendMessage("@navergooglekeyword", keyword_number + ", " + time_config)
            r += 1
    '''

elif switch == 0:
    naver_filter_list = already_keyword_list[:100]
    naver_filter_list = [v for v in naver_filter_list if v]
    cnt_naver_filter_list = len(naver_filter_list)
    value = 0
    while True:
        complete_expect_click_list = [-1]*len(naver_filter_list)
        complete_cost_click_list = [-1]*len(naver_filter_list)
        complete_bid_list = [-1]*len(naver_filter_list)
        temp_expect_click_list = complete_expect_click_list
        temp_cost_click_list = complete_cost_click_list
        temp_bid_list = complete_bid_list
        print("입찰가 등 정보 수집 시작")
        start = time.time()
        bot.sendMessage("@navergooglekeyword", "입찰가 등 정보 수집 시작")
        driver.get(keyword_naver_url)
        time.sleep(1)
        naver_total = []
        expect_click = 0
        keyword_enter_sheet = "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[2]/div/div/form/div[1]/textarea"
        element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[2]/div/div/form/div[1]/textarea")))
        driver.execute_script("arguments[0].click();", element)
        keyword_enter = driver.find_element_by_xpath(keyword_enter_sheet)
        time.sleep(1)

        for i in naver_filter_list:
            keyword_enter.send_keys(i)
            keyword_enter.send_keys(Keys.ENTER)
            time.sleep(0.5)
        element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[2]/div/div/form/div[2]/button[2]")))
        driver.execute_script("arguments[0].click();", element)
        time.sleep(2)
        bid_price = driver.find_element_by_xpath("/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-estimate/div[3]/div[2]/div/div[1]/div[1]/div/elena-input-amt/div/input")

        for i in range(70, 10001, 50):
            time.sleep(1)
            element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-estimate/div[3]/div[2]/div/div[1]/div[1]/div/elena-input-amt/div/input")))
            driver.execute_script("arguments[0].click();", element)
            bid = i
            bid_price.clear()
            bid_price.send_keys(bid)
            element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-estimate/div[3]/div[2]/div/div[1]/div[4]/button")))
            driver.execute_script("arguments[0].click();", element)
            time.sleep(2)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            click = soup.select("td.elenaColumn-clicks")
            cost = soup.select("td.elenaColumn-cost")
            expect_click_list = []
            cost_list = []

            for j in click:
                j = j.text.strip()
                j = j.replace(",", "")
                j = int(j)
                expect_click = j
                expect_click_list.append(expect_click)

            for k in cost:
                k = k.text.strip()
                k = k.strip("원")
                k = k.replace(",", "")
                k = k.strip()
                k = int(k)
                cost_list.append(k)

            for l in range(len(naver_filter_list)):
                idx_already_price = already_total_keyword_list.index(naver_filter_list[l])
                if (expect_click_list[l] >= already_total_price_list[idx_already_price] + 30) and complete_expect_click_list[l] < 0:
                    complete_expect_click_list[l] = expect_click_list[l]
                    complete_cost_click_list[l] = cost_list[l]
                    complete_bid_list[l] = bid

        for i in range(len(naver_filter_list)):
            idx_price = already_total_keyword_list.index(naver_filter_list[i])
            idx_google = already_keyword_list.index(naver_filter_list[i])
            naver_total.append([naver_filter_list[i], int(already_google_price_list[idx_google]), int(already_total_price_list[idx_price]), complete_expect_click_list[i], complete_bid_list[i], complete_cost_click_list[i], date])

        time.sleep(1)
        value_for_doc = "naver!" + "C" + str(value+1)
        doc.values_update(value_for_doc, params={'valueInputOption': 'RAW'}, body={'values': naver_total})
        time.sleep(10)
        print(r, time.time()-start)
        time_config = str(time.time()-start)
        keyword_number = str(r)
        bot.sendMessage("@navergooglekeyword", "반복 횟수는: " + keyword_number + ", 걸린 시간은: " + time_config + ", 검색한 Keyword 갯수는 :" + str(len(naver_filter_list)))
        r += 1
        naver_filter_list = already_keyword_list[cnt_naver_filter_list:cnt_naver_filter_list+100]
        naver_filter_list = [v for v in naver_filter_list if v]
        value += cnt_naver_filter_list

if switch == 0:
    print("입찰가를 비롯한 정보 수집 완료")
    bot.sendMessage("@navergooglekeyword", "입찰가를 비롯한 정보 수집 완료")
'''
elif len(already_keyword_list) >= 15000 and m == 0:
    for i in range(len(already_keyword_list)):
        driver.get(keyword_naver_url)
        time.sleep(1)
        keyword_enter_sheet = "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[2]/div/div/form/div[1]/textarea"
        element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[2]/div/div/form/div[1]/textarea")))
        driver.execute_script("arguments[0].click();", element)
        keyword_enter = driver.find_element_by_xpath(keyword_enter_sheet)
        time.sleep(1)
        keyword_enter.send_keys(already_keyword_list[i])
        time.sleep(1)
        element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[2]/div/div/form/div[2]/button[2]")))
        driver.execute_script("arguments[0].click();", element)
        time.sleep(2)
        bid_price = driver.find_element_by_xpath("/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-estimate/div[3]/div[2]/div/div[1]/div[1]/div/elena-input-amt/div/input")
        start = time.time()
        for j in range(70, 100001, 50):
            time.sleep(1)
            element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-estimate/div[3]/div[2]/div/div[1]/div[1]/div/elena-input-amt/div/input")))
            driver.execute_script("arguments[0].click();", element)
            n = j
            bid_price.clear()
            bid_price.send_keys(n)
            element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-estimate/div[3]/div[2]/div/div[1]/div[4]/button")))
            driver.execute_script("arguments[0].click();", element)
            time.sleep(2)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            click = soup.select("td.elenaColumn-clicks")
            cost = soup.select("td.elenaColumn-cost")
            cost_list = []
            for j in click:
                j = j.text.strip()
                j = j.replace(",", "")
                j = int(j)
                expect_click = j
            for k in cost:
                k = k.text.strip()
                k = k.strip("원")
                k = k.replace(",", "")
                k = k.strip()
                k = int(k)
                cost_list.append(k)
            if j >= already_price_list[i] + 30:
                date = now.strftime('%Y-%m-%d %H:%M:%S')
                naver_total.append([already_keyword_list[i], already_price_list[i], j, n, cost_list[0], date])
                break
            time.sleep(1)
        worksheet.insert_row(naver_total[i], i+1)
        time.sleep(10)
        print(r, time.time()-start)
        time_config = str(time.time()-start)
        keyword_number = str(r)
        bot.sendMessage("@navergooglekeyword", keyword_number + ", " + time_config)
        r += 1
'''

'''
except:
    print("이번 수행에서 추가한 Keyword의 개수: ", new_keyword_number)
    print("이번 수행에서 검색한 Keyword의 개수: ", r)
    bot.sendMessage("@navergooglekeyword", "오류 발생으로 작동을 중단합니다.")
    if new_keyword_number != 0:
        bot.sendMessage("@navergooglekeyword", "이번 수행에서 추가한 Keyword의 개수: " + str(new_keyword_number))
    if r != 0:
        bot.sendMessage("@navergooglekeyword", "이번 수행에서 검색한 Keyword의 개수: " + str(r))
'''