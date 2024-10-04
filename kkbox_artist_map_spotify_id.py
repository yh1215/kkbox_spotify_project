import csv
import requests
from bs4 import BeautifulSoup
import time
import random
from tqdm import tqdm

def read_artist_csv(file_path):
    artists = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            artist_name = row['spotify_artist']
            # 檢查是否已經存在該 artist
            if artist_name not in [artist['artist'] for artist in artists]:
                artists.append({
                    'artist': artist_name
                })
    return artists

def search_google_artist(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url, headers=headers)
    return response.text

def extract_spotify_artist_id(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for a in soup.find_all('a', href=True):
        if 'https://open.spotify.com/artist/' in a['href']:
            artist_url = a['href'].split('&')[0]
            return artist_url.split('/')[-1]
    return None

def scrape_spotify_artist_ids(artists):
    results = []
    for artist in tqdm(artists, desc="處理藝人", unit="位"):
        query = f"{artist['artist']} spotify"
        html_content = search_google_artist(query)
        spotify_id = extract_spotify_artist_id(html_content)
        results.append({
            'artist': artist['artist'],
            'spotify_id': spotify_id
        })
        time.sleep(random.uniform(1, 3))  # 添加隨機延遲，避免被封鎖
    return results

def save_results(results, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['artist', 'spotify_id'])
        writer.writeheader()
        writer.writerows(results)

def main():
    input_file = 'na_artist.csv'
    output_file = 'na_artist_merge.csv'
    
    print("開始讀取藝人資料...")
    artists = read_artist_csv(input_file)
    print(f"總共讀取了 {len(artists)} 位藝人")
    
    print("開始爬取 Spotify 藝人 ID...")
    results = scrape_spotify_artist_ids(artists)
    
    print("保存結果...")
    save_results(results, output_file)
    print(f"結果已保存到 {output_file}")

if __name__ == "__main__":
    main()