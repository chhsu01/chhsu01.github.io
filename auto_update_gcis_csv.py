import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 設定目標資料集名稱（可依實際需求修改）
TARGET_DATASET_NAME = '公司登記基本資料'
# 本地儲存 CSV 路徑
LOCAL_CSV_PATH = 'BGMOPEN1.csv'
# GCIS 開放資料首頁
GCIS_DATA_URL = 'https://data.gcis.nat.gov.tw/main/index'

def fetch_latest_dataset_info():
    """解析 GCIS 開放資料頁面，取得目標資料集的下載連結與更新日期"""
    resp = requests.get(GCIS_DATA_URL)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    for row in soup.select('tr'):
        cols = row.find_all('td')
        if len(cols) < 3:
            continue
        dataset_name = cols[0].get_text(strip=True)
        update_date = cols[1].get_text(strip=True)
        download_link = None
        for a in cols[2].find_all('a'):
            if 'csv' in a.get('href', '').lower():
                download_link = a['href']
                break
        if dataset_name == TARGET_DATASET_NAME and download_link:
            # 有些連結是相對路徑
            if not download_link.startswith('http'):
                download_link = 'https://data.gcis.nat.gov.tw' + download_link
            return update_date, download_link
    return None, None

def get_local_update_date():
    """取得本地 CSV 最後修改日期（格式：YYYY/MM/DD）"""
    if not os.path.exists(LOCAL_CSV_PATH):
        return None
    ts = os.path.getmtime(LOCAL_CSV_PATH)
    return datetime.fromtimestamp(ts).strftime('%Y/%m/%d')

def download_csv(download_url):
    print(f'下載最新 CSV: {download_url}')
    resp = requests.get(download_url)
    with open(LOCAL_CSV_PATH, 'wb') as f:
        f.write(resp.content)
    print('下載完成並覆蓋本地檔案')

def main():
    print('--- GCIS 公司登記自動更新腳本 ---')
    update_date, download_url = fetch_latest_dataset_info()
    if not update_date or not download_url:
        print('找不到最新資料集連結，請檢查目標網站格式是否變動')
        return
    local_update_date = get_local_update_date()
    print(f'線上最新更新日期: {update_date}')
    print(f'本地檔案更新日期: {local_update_date}')
    if local_update_date != update_date:
        download_csv(download_url)
        print('本地資料已更新！')
    else:
        print('本地資料已是最新，無需下載')

if __name__ == '__main__':
    main()
