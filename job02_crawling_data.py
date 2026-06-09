from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

# ── 드라이버 설정 ──────────────────────────────────────────
options = ChromeOptions()
options.add_argument('--lang=ko_KR')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')
options.add_argument('--headless')  # 브라우저창 안 보기 (속도 향상)

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 각 섹션별 메인 레이아웃의 div 번호 및 저장할 파일명 설정
sections = [
    ['Politics', '100', 4, 'naver_news_politics.csv'],
    ['Economics', '101', 5, 'naver_news_economics.csv'],
    ['Social', '102', 4, 'naver_news_social.csv'],
    ['Culture', '103', 4, 'naver_news_culture.csv'],
    ['World', '104', 4, 'naver_news_world.csv'],
    ['IT', '105', 4, 'naver_news_IT.csv']
]

os.makedirs('./data', exist_ok=True)

for category, section_num, div_num, file_name in sections:
    url = 'https://news.naver.com/section/{}'.format(section_num)
    print(f'\n[{category}] 크롤링 시작 → {url}')

    driver.get(url)
    time.sleep(2)

    # ── 더보기 버튼 30번 클릭 ──────────────────────────────
    button_xpath = '//*[@id="newsct"]/div[{}]/div/div[2]/a'.format(div_num)

    for i in range(30):
        try:
            btn = driver.find_element(By.XPATH, button_xpath)
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.7)
            print(f'  더보기 클릭 {i + 1}/30', end='\r')
        except Exception as e:
            print(f'\n  {i + 1}번째 클릭에서 중단됨 (기사가 더 없거나 로딩 지연)')
            break

    print(f'\n  더보기 클릭 완료! 기사 제목 추출 중...')

    # ── 기사 제목 수집 ─────────────────────────────────────
    titles = []

    # 안전하게 해당 div 구역 내부의 기사 클래스명(sa_text_strong)만 전부 추출
    title_xpath = '//*[@id="newsct"]/div[{}]//strong[contains(@class, "sa_text_strong")]'.format(div_num)
    title_tags = driver.find_elements(By.XPATH, title_xpath)

    for tag in title_tags:
        title_text = tag.text.strip()
        if title_text:
            titles.append(title_text)

    # 중복 제거 (순서 유지)
    titles = list(dict.fromkeys(titles))

    # ── 섹션별 개별 파일 저장 ─────────────────────────────────
    df_section = pd.DataFrame(titles, columns=['titles'])
    df_section['category'] = category

    # 지정한 파일명으로 개별 저장합니다.
    save_path = './data/{}'.format(file_name)
    df_section.to_csv(save_path, index=False, encoding='utf-8-sig')

    print(f'  🎉 {file_name} 저장 완료: {len(titles)}개')
    print('-' * 50)

driver.quit()
print('\n 모든 섹션이 개별 파일로 분리 저장되었습니다.')