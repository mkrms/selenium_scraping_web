from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
import csv

# Chromeの実行可能ファイルの場所を指定
service = Service('/usr/local/bin/chromedriver')

# Webdriverを起動し、URLにアクセスする
driver = webdriver.Chrome(service=service)

# Webdriverのタイムアウト時間を10秒に設定
wait = WebDriverWait(driver, 10)

# 取得したい要素があるセレクタ
target_selector = "h3.fanclub-name a"

# 取得したリンクを格納するためのリスト
links = []

account_links = []
names = []
twitter_links = []
fans = []

# CSVファイル名
csv_filename = "voice.csv"

# 最終行を取得する関数
def get_last_row(csv_filename):
    with open(csv_filename, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        last_row = None
        for row in reader:
            last_row = row
    return last_row

# 最終行を取得
last_row = get_last_row(csv_filename)

# ページ番号の初期値
page_number = 1

# voice_page 232
# voiceactor_page  52
# idol_page 26
# youtube_page 38
# photo_movie_page 118

#CSVファイルを追記モードで開く
with open(csv_filename, "a", newline="", encoding="utf-8") as csvfile:

# CSVファイルを上書きモードで開く
#with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    #csv_writer.writerow(["base_link", "name", "account_link", "twitter_link"])

    #while page_number <= 1:
    while page_number <= 100:

        # URLを再生成
        #url = f"https://fantia.jp/fanclubs?category=vtuber&order=newer&page={page_number}&brand_type=0"
        #url = f"https://fantia.jp/fanclubs?category=cosplay&order=newer&page={page_number}&brand_type=0"
        url = f"https://fantia.jp/fanclubs?category=voice&order=newer&page={page_number}&brand_type=0"
        #url = f"https://fantia.jp/fanclubs?category=voiceactor&order=newer&page={page_number}&brand_type=0"
        #url = f"https://fantia.jp/fanclubs?category=idol&order=newer&page={page_number}&brand_type=0"
        #url = f"https://fantia.jp/fanclubs?category=youtuber&order=newer&page={page_number}&brand_type=0"
        #url = f"https://fantia.jp/fanclubs?category=photo_movie&order=newer&page={page_number}&brand_type=0"


        links.append(url)

        # URLにアクセス
        driver.get(url)

        # 要素が存在するまで待機
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_selector)))

        next_link = driver.find_elements(By.CSS_SELECTOR, "li.num.ng-scope a")

        # 要素が存在するまで待機
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_selector)))

        # 要素を取得し、リンクとタイトルを取得してリストに追加
        elems = driver.find_elements(By.CSS_SELECTOR, target_selector)
        for elem in elems:
            link = elem.get_attribute("href")
            title = elem.get_attribute("title")
            account_links.append(link)
            names.append(title)
            # links.append({"title": title, "link": link})

        # 次のページがある場合、ページ番号を増やしてループを続ける
        if len(next_link) > 0:
            page_number += 1
            time.sleep(3)
        else:
            # 次のページが存在しない場合はループを終了
            break

    # 取得したリンクにアクセスして、Twitterのリンクを取得する
    for account_link in account_links:
        driver.get(account_link)
        time.sleep(3)  # ページが読み込まれるまで待機
        elems = driver.find_elements(By.CSS_SELECTOR, "div.btns.mt-10 a")
        fan_elems = driver.find_elements(By.CSS_SELECTOR, "span.text-primary.fan-count-inner span")
        
        # Twitterリンクが見つかったかどうかのフラグ
        found_twitter_link = False

        # ファン数が見つかったかどうかのフラグ
        found_fun_num = False

        for elem in elems:
            url = elem.get_attribute("href")
            # Twitterのリンクで、intentを含まない場合はurlを追加
            if url.startswith("https://twitter.com/") and "intent" not in url:
                twitter_links.append(url)
                found_twitter_link = True
                break

        for fan_elem in fan_elems:
            fan_num = fan_elem.text
            fans.append(fan_num)
            found_fun_num = True
            break
    
        # Twitterリンクが見つからない場合、空白を追加
        if not found_twitter_link:
            twitter_links.append("")

        # ファン数が見つからない場合、空白を追加
        if not found_fun_num:
            fans.append("")


    #二次元配列の転置
    data = [names, account_links, twitter_links, fans]

    transposed_data = list(map(list, (zip(*data))))
    print(transposed_data)

    account_per_link = 24

    for i, link in enumerate(links):
        # Step 1 and 4: Insert link data
        csv_writer.writerow([link])

        # Step 2 and 5: Insert transposed_data
        start_index = i * account_per_link
        end_index = start_index + account_per_link
        for row in transposed_data[start_index:end_index]:
            csv_writer.writerow(row)

        # Step 3 and 6: Insert an empty line
        csv_writer.writerow([])

# 結果を出力
#print("取得したリンク数：", len(account_links))
#print("取得したTwitterリンク数：", len(twitter_links))
