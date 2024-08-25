def process_artists(df):
    artist = df[df['artist_id'] != '#'][['artist', 'artist_id']].drop_duplicates()
    return artist