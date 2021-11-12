import pandas as pd
import numpy as np

df = pd.read_csv('junggu.csv', sep=',')
df = df.loc[df['영업상태명'] == '영업/정상'] 

df = df[['사업장명', '전화번호', '소재지면적', '소재지우편번호', '지번주소', '도로명주소', '도로명우편번호', '업태구분명', '시설총규모']]
search_location_list = ['을지로1가','을지로2가','을지로3가','을지로4가', '을지로5가', '을지로6가','을지로7가','주교동', '초동', '방산동',  '입정동', '산림동', '인현동1가', '저동2가']
search_location = '|'.join(search_location_list)

df_q = df[df['지번주소'].str.contains(search_location, na=False)]

df_q.columns = ['name',   # 사업장명
              'telno',  # 전화번호
              'size',   # 소재지면적
              'pstno',  # 소재지우편번호
              'addr',   # 지번주소
              'addr2',  # 도로명주소
              'pstno2',  # 도로명우편번호
              'categ',   # 업태구분명
              'restr_sise' # 시설총규모
              ]

print(df_q)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import random

chromedriver = 'C:\\chromedriver\\chromedriver.exe' 
driver = webdriver.Chrome(chromedriver) 

df_q['keyword'] = '을지로' + "%20" + df_q['name']  
df_q['map_url'] = ''

for i, keyword in enumerate(df_q['keyword'].tolist()):
    print("keyword :", i, f"/ {df_q.shape[0] -1} row", keyword)
    try:
        naver_map_search_url = f"https://m.map.naver.com/search2/search.naver?query={keyword}&sm=hty&style=v5"
        
        driver.get(naver_map_search_url)
        time.sleep(random.randrange(1,30))
        df_q.iloc[i,-1] = driver.find_element_by_css_selector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview").get_attribute('data-cid')

    except Exception as e1:
        if "li:nth-child(1)" in str(e1):  
            try:
                df_q.iloc[i,-1] = driver.find_element_by_css_selector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview").get_attribute('data-cid')
                time.sleep(1)
            except Exception as e2:
                print(e2)
                df_q.iloc[i,-1] = np.nan
                time.sleep(1)
        else:
            pass

df_q['map_url'] = "https://m.place.naver.com/restaurant/" + df_q['map_url'] 
driver.quit()
df_q = df_q.loc[~df_q['map_url'].isnull()]
df_q.to_excel('url_info.xlsx')

