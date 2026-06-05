 # 파일명은 naver_news_section.csv로 해주세요.
 # 컬럼명은 titles, category로 해주세요.
 # 00님이 정치, 경제
 # 01님이 사회, 문화
 # 02님이 세계, IT
 # 다 되면 PR부탁합니다.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import pandas as pd

options = ChromeOptions()
options.add_argument("lang=ko_KR")
options.add_argument("headless") # 브라우저 안봄

os.environ['WDM_LOCAL'] = '1'
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

os.makedirs('./data', exist_ok=True)


def save_news_section(url, category, file_name):
    driver.get(url)
    button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]/a'
    for i in range(30):
        driver.find_element(By.XPATH, button_xpath).click()
        time.sleep(0.5)

    titles = []
    title_tags = driver.find_elements(
        By.XPATH,
        '//*[@id="newsct"]/div[4]/div/div[1]//strong[contains(@class, "sa_text_strong")]'
    )
    for title_tag in title_tags:
        title = title_tag.text
        if title:
            titles.append(title)

    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category
    df_section_titles.to_csv('./data/{}'.format(file_name), index=False)
    print('{} 저장 완료: {}개'.format(file_name, len(titles)))


try:
    save_news_section('https://news.naver.com/section/102', 'Social', 'naver_news_social.csv')
    save_news_section('https://news.naver.com/section/103', 'Culture', 'naver_news_culture.csv')
finally:
    driver.quit()
