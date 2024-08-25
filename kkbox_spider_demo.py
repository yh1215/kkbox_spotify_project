# extract to one csv file
import pandas as pd
import requests
import re
import json
from datetime import datetime, timedelta
import os

def get_data(date, cate=None):
    if cate:
        url = f"https://kma.kkbox.com/charts/daily/song?cate={cate}&date={date}&lang=tc&terr=tw"
    else:
        url = f"https://kma.kkbox.com/charts/daily/song?date={date}&lang=tc&terr=tw"
    
    response = requests.get(url)
    content = response.text

    # 設置 category
    category_map = {
        '390': 'western',
        '308': 'japanese',
        '314': 'kpop',
        '304': 'taiwanese',
        '320': 'cantonese',
        None: 'mandarin'
    }
    category = category_map.get(cate, 'mandarin')

    # 尋找包含數據的 JavaScript 變量
    match = re.search(r'var\s+chart\s*=\s*(\[.*?\]);', content, re.DOTALL)
    if match:
        chart_data = json.loads(match.group(1))
        
        daily_data = []
        for song in chart_data:
            song_data = {
                "rank": song['rankings']['this_period'],
                "artist": song.get('artist_name', ''),
                "artist_id": song.get('artist_url', '').split('/')[-1] if song.get('artist_url') else '',
                "song_id": song.get('song_url', '').split('/')[-1] if song.get('song_url') else '',
                "album_id": song.get('album_url', '').split('/')[-1] if song.get('album_url') else '',
                "date": date,
                "category": category
            }
            daily_data.append(song_data)
        
        return daily_data
    return []

# 設置日期範圍
start_date = datetime(2021, 1, 1)
end_date = datetime(2021, 1, 31)

# 確保輸出目錄存在
os.makedirs('kkbox_data', exist_ok=True)

# 定義要爬取的類別
categories = [None, '390', '308', '314', '304', '320']

# 收集所有数据
all_data = []

# 爬取每一天的數據
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime('%Y-%m-%d')
    
    for cate in categories:
        print(f"爬取 {date_str} 的數據，類別: {cate if cate else 'mandarin'}...")

        daily_data = get_data(date_str, cate)
        
        if daily_data:
            all_data.extend(daily_data)
        else:
            print(f"無法獲取 {date_str} 的數據，類別: {cate if cate else 'mandarin'}")

    current_date += timedelta(days=1)

# 將所有數據轉換為DataFrame
df = pd.DataFrame(all_data)

# 保存為CSV文件
csv_filename = "kkbox_data/kkbox_data.csv"
df.to_csv(csv_filename, index=False, encoding='utf-8-sig')

print(f"保存數據到 {csv_filename} 完成！")