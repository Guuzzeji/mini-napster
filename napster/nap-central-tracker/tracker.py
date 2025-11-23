from flask import Flask, jsonify, request
import uuid
import sys

app = Flask(__name__)

files = {}
file_to_users = {}

if len(sys.argv) > 1:
    SERVER_PORT = int(sys.argv[1])
else:
    SERVER_PORT = 3030

def print_db():
    print("==== Current files in tracker ====")
    for file_id, data in files.items():
        print(f"File ID: {file_id}")
        for key, value in data.items():
            print(f"  {key}: {value}")

    print("\n==== Current users in tracker ====")
    for file_id, user_id in file_to_users.items():
        print(f"File ID: {file_id}, User ID: {user_id}")


@app.route('/user/upload-metadata', methods=['POST'])
def upload_metadata():
    data = request.json

    required_fields = ['user_id', 'song_name', 'artist', 'checksum']
    for field in required_fields: 
        if field not in data:
            return { 'error': f'{field} is required' }, 400
    
    if data['file_id'] and data['file_id'] in files.keys():
        if file_to_users[data['file_id']] == data['user_id']:
            return {'file_id': '' }, 400

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
    file_to_users[file_id] = user_id  

    # debug print
    print(f"Uploaded metadata for file_id: {file_id}, user_id: {user_id}")
    print_db()

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
            result = {
                'file_id': file_id,
                'song_name': file_data['song_name'],
                'artist': file_data['artist'],
                'user_id': file_to_users[file_id]
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
    if file_id not in file_to_users:
        return {'error': 'File not found'}, 404
    

    # Store as username|ip|port
    user = file_to_users[file_id].split('|')

    return {
        'file_id': file_id,
        'port': int(user[2]),
        'file_name': files[file_id]['song_name'],
        'user_ip': user[1],
        'username': user[0],
        'checksum': files[file_id]['checksum']  
    }, 200

if __name__ == '__main__':
    print(f"Starting Tracker Server on port {SERVER_PORT}")
    app.run(host='0.0.0.0', port=SERVER_PORT, debug=True)