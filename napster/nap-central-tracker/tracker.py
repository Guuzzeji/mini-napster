from flask import Flask, jsonify, request
import uuid
from datetime import datetime

app = Flask(__name__)

files = {}
file_to_users = {}

DEFAULT_SERVER_PORT = 5000

@app.route('/user/upload-metadata', methods=['POST'])
def upload_metadata():
    data = request.json

    required_fields = ['user_id', 'song_name', 'artist', 'checksum']
    for field in required_fields: 
        if field not in data:
            return { 'error': f'{field} is required' }, 400
        
    user_id = data['user_id']
    file_id = str(uuid.uuid4())[:8] # Shorten UUID for simplicity for Demo

    files[file_id] = {
        'song_name': data['song_name'],
        'artist': data['artist'],
        'album': data.get('album', ''),
        'duration': data.get('duration', 0),
        'file_size': data.get('file_size', 0),
        'year': data.get('year', ''),
        'checksum': data['checksum'],
        'id': file_id
    }
    file_to_users[file_id] = [user_id]  
    return {'file_id': file_id}, 200

@app.route('/search', methods=['GET'])
def search_files():
    artist = request.args.get('artist', '')
    song = request.args.get('song', '')
    
    if not artist and not song:
        return jsonify({'error': 'Provide at least artist or song parameter'}), 400
    
    results = []
    
    for file_id, file_data in files.items():
        artist_match = artist.lower() in file_data['artist'].lower() if artist else True
        song_match = song.lower() in file_data['song_name'].lower() if song else True
        
        if artist_match and song_match:
            available_users = []
            for user_id in file_to_users.get(file_id, []):
                available_users.append({
                    'ip_address': '127.0.0.1',  
                    'port': 8080
                })
            
            if available_users:
                result = {
                    'file_id': file_id,
                    'song_name': file_data['song_name'],
                    'artist': file_data['artist'],
                    'available_users': available_users
                }
                
                # Add optional fields
                if file_data.get('album'):
                    result['album'] = file_data['album']
                if file_data.get('duration'):
                    result['duration'] = file_data['duration']
                if file_data.get('file_size'):
                    result['file_size'] = file_data['file_size']
                if file_data.get('year'):
                    result['year'] = file_data['year']
                
                results.append(result)
    
    return jsonify(results), 200

@app.route('/download', methods=['GET'])
def get_download_info():
    file_id = request.args.get('file_id')
    if not file_id:
        return {'error': 'File ID is required'}, 400
    if file_id not in files:
        return {'error': 'File not found'}, 404
    
    return {
        'file_id': file_id,
        'port': 8080,
        'user_ip': '127.0.0.1',
        'checksum': files[file_id]['checksum']  
    }, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)