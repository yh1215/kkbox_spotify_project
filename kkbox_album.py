def process_albums(df):
    album_id = df[df['album_id'] != '#']['album_id'].drop_duplicates()

    from kkbox_developer_sdk.auth_flow import KKBOXOAuth

    auth = KKBOXOAuth('5e5e2e22f6e9940a106b3befde703767', 'd3aa398ae0aa2018b5205a6a98692a4d')
    token = auth.fetch_access_token_by_client_credentials()
    access_token = token.access_token

    import http.client
    import json

    conn = http.client.HTTPSConnection("api.kkbox.com")
    headers = {
        'accept': "application/json",
        'authorization': f"Bearer {access_token}"
    }
    
    from tqdm import tqdm
    import time
    import pandas as pd

    results = []

    for id in tqdm(album_id):
        try:
            conn.request("GET", f"/v1.1/albums/{id}?territory=TW", headers=headers)
            res = conn.getresponse()
            data = res.read()
            
            album_data = json.loads(data.decode("utf-8"))
            
            album_name = album_data.get("name")
            album_id = album_data.get("id")
            release_date =album_data.get("release_date")
            
            results.append({"name": album_name, "album_id": album_id, "release_date": release_date})
            
            time.sleep(0.1)
        
        except Exception as e:
            print(f"Error processing album ID {id}: {str(e)}")

    # Create a DataFrame from the results
    albums_df = pd.DataFrame(results)
    return albums_df