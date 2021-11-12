import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup


# 각 데이터들을 미리 리스트에 담은 다음, 마지막에 데이터 프레임에 합칠 것입니다.
title_list = []
naver_map_menu_list = []
blog_review_list = []
blog_review_qty_list = []
naver_map_star_review_stars_list = []
naver_map_star_review_qty_list = []
naver_map_type_list = []

chromedriver = 'C:\\chromedriver\\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
# 서브 드라이버 : 블로그 리뷰 텍스트를 리뷰 탭 들어가서 크롤링
sub_driver = webdriver.Chrome(chromedriver) 
# 서브 드라이버2 : 메뉴 크롤링
sub_driver2 = webdriver.Chrome(chromedriver) 

df = pd.read_excel('url_info.xlsx')

for i, url in enumerate(df['map_url']):
   
    print(url)
    if url == "https://m.place.naver.com/restaurant/":
        pass
    driver.get(url)
    sub_driver.get(url+"/review/ugc")
    sub_driver2.get(url+"/menu/list")
    time.sleep(2)


    try:

        # 간단 정보 가져오기
        title = driver.find_element_by_css_selector("#_title > span._3XamX").text
        # 네이버 지도의 유형 분류
        naver_map_type = driver.find_element_by_css_selector("#_title > span._3ocDE").text
        # 블로그 리뷰 수
        blog_review_qty = driver.find_element_by_css_selector("#app-root > div > div > div.place_detail_wrapper > div.place_section.no_margin.GCwOh > div > div > div._3XpyR > div > span:nth-child(3) > a > em").text
        # 블로그 별점 점수
        star_review_stars = driver.find_element_by_css_selector("#app-root > div > div > div.place_detail_wrapper > div.place_section.no_margin.GCwOh > div > div > div._3XpyR > div > span._1Y6hi._1A8_M > em").text
        # 블로그 별점 평가 수
        star_review_qty = driver.find_element_by_css_selector("#app-root > div > div > div.place_detail_wrapper > div.place_section.no_margin.GCwOh > div > div > div._3XpyR > div > span:nth-child(2) > a > em").text
       
        # 블로그 리뷰 텍스트 가져오기
        review_text_list = [] # 임시 선언
        review_text = ''
        menu_text = ''

        # 네이버 지도 블로그 리뷰 탭은 동적 웹사이트의 순서가 주문하기, 메뉴보기 등의 존재 여부로 다르기 때문에 css selector가 아니라 element 찾기로 진행
        review_text_crawl_list = sub_driver.find_elements_by_class_name("_2CbII")        
        # find element's' 메소드를 통해 가져온 내용은 리스트로 저장되고, 리스트 타입을 풀어서(for문 사용) 임시 데이터에 모아 두어야 한다
        for review_crawl_data in review_text_crawl_list:
            review_text_list.append(review_crawl_data.find_element_by_tag_name('div').text)        
        # 그 리스트에 저장된 텍스트 (한 식당에 대한 여러 리뷰들)를 한 텍스트 덩어리로 모아(join)줍니다.
        review_text = ','.join(review_text_list)
        

        # 메뉴 찾기
        temp = sub_driver2.find_elements_by_class_name("_2CZ7z")
        menu_list = [] # 임시 선언
        for menu in temp:            
            menu_list.append(menu.find_element_by_tag_name('div').text)             
        menu_text = ','.join(menu_list)
        
        blog_review_list.append(review_text)
        title_list.append(title)
        naver_map_menu_list.append(menu_text)
        naver_map_type_list.append(naver_map_type)
        blog_review_qty_list.append(blog_review_qty)
        naver_map_star_review_stars_list.append(star_review_stars)
        naver_map_star_review_qty_list.append(star_review_qty)

    # 리뷰가 없는 업체는 크롤링에 오류가 뜨므로 표기해둡니다.
    except Exception as e1:
        print(f"{i}행 문제가 발생")
        
        # 리뷰가 없으므로 null을 임시로 넣어줍니다
        if menu_text == '':
            naver_map_menu_list.append('null')
        else:
            naver_map_menu_list.append(menu_text)
        if blog_review_list == '':
            blog_review_list.append('null')
        else:
             blog_review_list.append(review_text)
        
        title_list.append(title)        
        naver_map_type_list.append(naver_map_type)
        blog_review_qty_list.append(blog_review_qty)
        naver_map_star_review_stars_list.append(star_review_stars)
        naver_map_star_review_qty_list.append(star_review_qty)
        
driver.quit()
sub_driver.quit()
sub_driver2.quit()



df['naver_title'] = title_list
df['naver_store_type'] = naver_map_type_list  # 네이버 상세페이지에서 크롤링한 업체 유형
df['naver_star_point'] = naver_map_star_review_stars_list  # 네이버 상세페이지에서 평가한 별점 평점
df['naver_star_point_qty'] = naver_map_star_review_qty_list  # 네이버 상세페이지에서 별점 평가를 한 횟수
df['naver_blog_review_txt'] = blog_review_list  # 네이버 상세페이지에 나온 블로그 리뷰 텍스트들
df['naver_blog_review_qty'] = blog_review_qty_list  # 네이버 상세페이지에 나온 블로그 리뷰의 총 개수
df['naver_menu'] = naver_map_menu_list

df.to_excel('./result.xlsx')