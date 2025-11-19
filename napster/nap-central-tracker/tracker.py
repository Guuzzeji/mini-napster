from flask import Flask, jsonify, request
import uuid
from datetime import datetime

app = Flask(__name__)

users = {}
files = {}
file_to_users = {}

def is_user_online(user):
    """Check if user was active in the last 60 seconds"""
    return (datetime.now() - user['last_checkin']).total_seconds() < 60

@app.route('/user/checkin', methods=['POST'])
def user_checkin():
    data = request.json

    user_id = data.get('user_id', str(uuid.uuid4()))
    users[user_id] = {
        'last_checkin': datetime.now(),
        'port': data['port'],
        'ip': request.remote_addr
    }
    return {'user_id': user_id}, 200

@app.route('/user/upload-metadata', methods=['POST'])
def upload_metadata():
    data = request.json

    required_fields = ['user_id', 'song_name', 'artist', 'checksum']
    for field in required_fields: 
        if field not in data:
            return { 'error': f'{field} is required' }, 400
        
    user_id = data['user_id']
    if user_id not in users:
        return {'error': 'User not found'}, 404
    
    file_id = str(uuid.uuid4())
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
                user = users.get(user_id)
                if user and is_user_online(user):
                    available_users.append({
                        'ip_address': user['ip'],  
                        'port': user['port']
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
    
    for user_id in file_to_users.get(file_id, []):
        user = users.get(user_id)
        if user and is_user_online(user):
            return {
                'file_id': file_id,
                'port': user['port'],
                'user_ip': user['ip'],
                'checksum': files[file_id]['checksum']  
            }, 200
    
    return {'error': 'No online users have this file'}, 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)