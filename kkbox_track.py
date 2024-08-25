def process_tracks(df):
    album_id = df[df['album_id'] != '#']['album_id'].drop_duplicates()
    # 這裡加入使用 KKBOX API 獲取歌曲詳細信息的代碼
    from kkbox_developer_sdk.auth_flow import KKBOXOAuth
    import http.client

    auth = KKBOXOAuth('5e5e2e22f6e9940a106b3befde703767', 'd3aa398ae0aa2018b5205a6a98692a4d')
    token = auth.fetch_access_token_by_client_credentials()
    access_token = token.access_token

    conn = http.client.HTTPSConnection("api.kkbox.com")
    headers = {
        'accept': "application/json",
        'authorization': f"Bearer {access_token}"
    }

    import json
    from tqdm import tqdm
    import time
    import pandas as pd


    # 創建一個列表來存儲所有歌曲的數據
    all_tracks = []

    for id in tqdm(album_id):
        try:
            conn.request("GET", f"/v1.1/albums/{id}/tracks?territory=TW&offset=0&limit=500", headers=headers)
            res = conn.getresponse()
            data = res.read()
            
            # Parse the JSON response
            track_data = json.loads(data.decode("utf-8"))
            
            # 提取每首歌曲的信息
            for track in track_data['data']:
                all_tracks.append({
                    'name': track['name'],
                    'id': track['id'],
                    'duration': track['duration'],
                    'track_number': track['track_number'],
                    'album_id': id  # 添加專輯ID以便追蹤
                })
            
            # 添加一個小延遲以避免過度請求API
            time.sleep(0.1)
        
        except Exception as e:
            print(f"處理專輯ID {id} 時發生錯誤: {str(e)}")

    # 將所有數據轉換為DataFrame
    df_track = pd.DataFrame(all_tracks)
    return df_track