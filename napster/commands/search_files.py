from napster.core.tracker_handler.tracker import search_file as tracker_search_file
from napster.core.tracker_handler.request_bodies import SearchFileResponseBody

def search_file(artist: str = '', song: str = ''):
    response = tracker_search_file(artist, song)
    if response is None or response.data == []:
        print("No files found")
        return

    print(f"== Found {len(response.data)} files ==")
    for file in response.data:
        print(f"- {file.song_name} by {file.artist} \n   > | File owned by {file.user_id.split('|')[0]} | ID: {file.file_id}, Size: {file.file_size} bytes |")