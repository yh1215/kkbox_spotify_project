import pandas as pd
from kkbox_spider import scrape_kkbox_data
from kkbox_artist import process_artists
from kkbox_album import process_albums
from kkbox_track import process_tracks
from datetime import datetime, timedelta

def main():
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2021, 1, 31)

    # Step 1: Scrape data
    df = scrape_kkbox_data(start_date, end_date)
    
    # Step 2: Process artists
    artists_df = process_artists(df)
    artists_df.to_csv('kkbox_data/artists.csv', index=False)
    
    # Step 3: Process albums
    albums_df = process_albums(df)
    albums_df.to_csv('kkbox_data/albums.csv', index=False)
    
    # Step 4: Process tracks
    tracks_df = process_tracks(df)
    tracks_df.to_csv('kkbox_data/tracks.csv', index=False)
    
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()