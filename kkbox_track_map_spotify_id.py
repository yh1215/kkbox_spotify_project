import csv
import requests
from bs4 import BeautifulSoup
import time
import random
from tqdm import tqdm

def read_csv(file_path):
    songs = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            songs.append({
                'track': row['track'],
                'artist': row['artist']
            })
    return songs

def search_google(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url, headers=headers)
    return response.text

def extract_spotify_id(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for a in soup.find_all('a', href=True):
        if 'https://open.spotify.com/track/' in a['href']:
            track_url = a['href'].split('&')[0]
            return track_url.split('/')[-1]
    return None

def scrape_spotify_ids(songs):
    results = []
    for song in tqdm(songs, desc="處理", unit="首"):
        query = f"{song['artist']} {song['track']} spotify"
        html_content = search_google(query)
        spotify_id = extract_spotify_id(html_content)
        results.append({
            'track': song['track'],
            'artist': song['artist'],
            'spotify_id': spotify_id
        })
        time.sleep(random.uniform(1, 3))  # 添加隨機延遲，避免被封鎖
    return results

def save_results(results, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['track', 'artist', 'spotify_id'])
        writer.writeheader()
        writer.writerows(results)

def main():
    input_file = 'track_without_spotify_id.csv'
    output_file = 'track_without_spotify_id_merge.csv'
    
    print("開始讀取資料...")
    songs = read_csv(input_file)
    print(f"總共讀取了 {len(songs)} 位藝人")
    
    print("開始爬取 SpotifyID...")
    results = scrape_spotify_ids(songs)
    
    print("保存結果...")
    save_results(results, output_file)
    print(f"結果已保存到 {output_file}")

if __name__ == "__main__":
    main()