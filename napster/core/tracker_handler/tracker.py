import requests

from napster.core.constants import TRACKER_SERVER_URL
from napster.core.tracker_handler.request_bodies import UploadMetadataResponseBody, UploadMetadataRequestBody, SearchFileResponseBody, DownloadInfoResponseBody

def upload_metadata(body: UploadMetadataRequestBody) -> UploadMetadataResponseBody | None:
    r = requests.post(
        f'{TRACKER_SERVER_URL}/user/upload-metadata',
        json=body.to_json())
    
    if r.status_code != 200:
        return None

    return UploadMetadataResponseBody.from_json(r.json())

def search_file(artist: str = '', song: str = '') -> SearchFileResponseBody | None:
    params = {}
    if artist:
        params['artist'] = artist
    if song:
        params['song'] = song

    r = requests.get(
        f'{TRACKER_SERVER_URL}/search',
        params=params)
    
    if r.status_code != 200:
        return None

    return SearchFileResponseBody.from_json(r.json())

def get_download_info(file_id: str) -> DownloadInfoResponseBody | None:
    r = requests.get(
        f'{TRACKER_SERVER_URL}/download',
        params={'file_id': file_id}
    )

    if r.status_code != 200:
        return None

    return DownloadInfoResponseBody.from_json(r.json())