from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from itertools import groupby
import requests
import re
import time
import lxml
import pandas as pd
import numpy as np
from operator import itemgetter
start = time.time()

driver = webdriver.Chrome("C:/Users/june/Desktop/chromedriver.exe")
url_naver = "https://searchad.naver.com/login"
id_naver = "lyrical98"
password_naver = "dmsgur!23"
search_total = []
naver_total = []

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
driver.switch_to.window(driver.window_handles[1])
driver.close()
driver.switch_to.window(driver.window_handles[0])
naver_class_n = ""
keyword_naver_url = "https://manage.searchad.naver.com/customers/1948785/tool/keyword-planner?keywords="

# 목록 수집
## 리스트 순회
for i in [3]: # , 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22
    time.sleep(2)
    keyword_naver_url = "https://manage.searchad.naver.com/customers/1948785/tool/keyword-planner?keywords="
    driver.get(keyword_naver_url)
    naver_class_check_url = "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/label"
    time.sleep(2)
    driver.find_element_by_xpath(naver_class_check_url).click()
    enter_button = "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[3]/button"
    time.sleep(2)
    naver_class_n = str(i)
    naver_class_1 = "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/div/li["
    naver_class_2 = naver_class_n
    naver_class_3 = "]/div"  # 3 ~ 22
    click_find = naver_class_1 + naver_class_2 + naver_class_3
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/button").click()
    driver.find_element_by_xpath(click_find).click()
    time.sleep(2)
    driver.find_element_by_xpath(enter_button).click()
    time.sleep(2)
    ## 검색어 추출
    for j in [4]: # , 5, 6, 7, 8, 9, 10, 11, 12, 13
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
        '''
        next_page_1 = "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[2]/div[3]/elena-table/elena-table-paginator/div/div/nav/ul/li["
        next_page_2 = str(j)
        next_page_3 = "]/a"
        next_page = next_page_1 + next_page_2 + next_page_3
        time.sleep(1)
        driver.find_element_by_xpath(next_page).click()
        time.sleep(1)
        '''
search_total.sort(key=lambda x:-x[1])  # 클릭수 높은 순서대로 정렬

# 목록 입력
search_range_start = 0  # search_range는 0 ~ 179까지 가능. 한 번에 100개씩임.
range_end = 178     # range_end는 178(한 번) ~ 0(179번)까지 가능.
for i in range(179-range_end):
    search_total_slice = search_total[(search_range_start)*100:(search_range_start+1)*100]
    print(search_total_slice)
    search_range_start += 1
    search_enter = []
    for j in search_total_slice:
        search_enter.append(j[0])
    driver.get(keyword_naver_url)
    time.sleep(1)
    keyword_enter_sheet = "/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[2]/div/div/form/div[1]/textarea"
    driver.find_element_by_xpath(keyword_enter_sheet).click()
    keyword_enter = driver.find_element_by_xpath(keyword_enter_sheet)
    time.sleep(1)
    for k in search_enter:
        keyword_enter.send_keys(k)
        keyword_enter.send_keys(Keys.ENTER)
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[2]/div/div/form/div[2]/button[2]").click()
    time.sleep(3)
    bid_price = driver.find_element_by_xpath("/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-estimate/div[3]/div[2]/div/div[1]/div[1]/div/elena-input-amt/div/input")
    pre, pre_past = [], []

    for i in range(70, 100001, 10):
        n = i
        bid_price.click()
        bid_price.clear()
        bid_price.send_keys(i)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-estimate/div[3]/div[2]/div/div[1]/div[4]/button").click()
        time.sleep(3)
        expect_name, expect_click, expect = [], [], []
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.select("td.elenaColumn-keyword")
        for i in name:
            i = i.text.strip()
            expect_name.append(i)
        click = soup.select("td.elenaColumn-clicks")
        for j in click:
            j = j.text.strip()
            j = j.replace(",", "")
            j = int(j)
            expect_click.append(j)
        for k in range(len(name)):
            expect.append([expect_name[k],expect_click[k]])

        for i in range(100):
            if expect[i][1] < search_total_slice[i][1] + 30:
                expect[i][1] = expect[i][1]
            elif expect[i][1] >= search_total_slice[i][1] + 30:
                expect[i][1] += 0

        if pre == expect:
            break
        else:
            pre = expect
        print(pre)