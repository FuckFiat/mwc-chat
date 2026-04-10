#!/usr/bin/env python3
"""
Fucking Miners Chat Server v2.0
С поддержкой личных сообщений и ответов
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Data storage
DATA_DIR = '/var/www/fucking-miners/data'
DATA_FILE = os.path.join(DATA_DIR, 'chat_data.json')

def ensure_data_dir():
    """Ensure data directory exists"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        logger.info(f"Created data directory: {DATA_DIR}")

def load_data():
    """Load data from file"""
    ensure_data_dir()
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading data: {e}")
    return {'users': {}, 'messages': []}

def save_data(data):
    """Save data to file"""
    ensure_data_dir()
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Data saved: {len(data.get('messages', []))} messages, {len(data.get('users', {}))} users")
    except Exception as e:
        logger.error(f"Error saving data: {e}")

# Initialize data
data = load_data()

@app.route('/')
def index():
    """Health check"""
    return jsonify({
        'status': 'online',
        'service': 'Fucking Miners Chat',
        'version': '2.0',
        'users': len(data.get('users', {})),
        'messages': len(data.get('messages', []))
    })

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Get all messages (public channel)"""
    # Return only public messages (no recipient)
    public_messages = [m for m in data.get('messages', []) if not m.get('recipient')]
    return jsonify(public_messages[-100:])

@app.route('/api/messages/private', methods=['GET'])
def get_private_messages():
    """Get private messages between users"""
    user1 = request.args.get('user1')
    user2 = request.args.get('user2')
    
    if not user1 or not user2:
        return jsonify({'error': 'Missing user1 or user2'}), 400
    
    # Get messages between these two users
    private_messages = [
        m for m in data.get('messages', [])
        if m.get('recipient') in [user1, user2] and m.get('user') in [user1, user2]
    ]
    
    return jsonify(private_messages[-100:])

@app.route('/api/messages', methods=['POST'])
def add_message():
    """Add a new message"""
    content = request.json
    
    message = {
        'id': str(int(datetime.now().timestamp() * 1000)),  # Unique ID
        'user': content.get('user'),
        'text': content.get('text'),
        'time': content.get('time', int(datetime.now().timestamp() * 1000)),
        'recipient': content.get('recipient'),  # For private messages
        'replyTo': content.get('replyTo'),  # For replies
        'channel': content.get('channel', 'fucking-miners')  # Channel
    }
    
    if not message['user'] or not message['text']:
        return jsonify({'error': 'Missing user or text'}), 400
    
    data['messages'].append(message)
    
    # Keep only last 1000 messages
    if len(data['messages']) > 1000:
        data['messages'] = data['messages'][-1000:]
    
    save_data(data)
    logger.info(f"New message from {message['user']}: {message['text'][:50]}...")
    
    return jsonify({'success': True, 'message': message})

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    return jsonify(data.get('users', {}))

@app.route('/api/users/<username>', methods=['GET'])
def get_user(username):
    """Get user by name"""
    user = data.get('users', {}).get(username)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/users', methods=['POST'])
def register_user():
    """Register or update user"""
    content = request.json
    username = content.get('username')
    
    if not username:
        return jsonify({'error': 'Missing username'}), 400
    
    user_data = {
        'password': content.get('password'),
        'avatar': content.get('avatar', username[0].upper()),
        'online': content.get('online', True),
        'createdAt': content.get('createdAt', int(datetime.now().timestamp() * 1000)),
        'lastSeen': int(datetime.now().timestamp() * 1000),
        'messageCount': content.get('messageCount', 0)
    }
    
    # If user exists, update only certain fields
    if username in data.get('users', {}):
        existing = data['users'][username]
        user_data['createdAt'] = existing.get('createdAt', user_data['createdAt'])
        user_data['messageCount'] = existing.get('messageCount', 0)
    
    data['users'][username] = user_data
    save_data(data)
    
    logger.info(f"User registered: {username}")
    return jsonify({'success': True, 'user': user_data})

@app.route('/api/users/<username>/online', methods=['POST'])
def set_online(username):
    """Set user online status"""
    content = request.json
    online = content.get('online', True)
    
    if username in data.get('users', {}):
        data['users'][username]['online'] = online
        data['users'][username]['lastSeen'] = int(datetime.now().timestamp() * 1000)
        save_data(data)
        return jsonify({'success': True})
    
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get chat statistics"""
    total_users = len(data.get('users', {}))
    online_users = sum(1 for u in data.get('users', {}).values() if u.get('online'))
    total_messages = len(data.get('messages', []))
    public_messages = len([m for m in data.get('messages', []) if not m.get('recipient')])
    private_messages = total_messages - public_messages
    
    return jsonify({
        'totalUsers': total_users,
        'onlineUsers': online_users,
        'totalMessages': total_messages,
        'publicMessages': public_messages,
        'privateMessages': private_messages,
        'uptime': str(datetime.now())
    })

@app.route('/api/clear', methods=['POST'])
def clear_messages():
    """Clear all messages"""
    data['messages'] = []
    save_data(data)
    logger.warning("Messages cleared")
    return jsonify({'success': True})

if __name__ == '__main__':
    print('=== Fucking Miners Chat Server v2.0 ===')
    print('Running on http://0.0.0.0:5004')
    print('')
    print('API endpoints:')
    print('  GET  /                    - Health check')
    print('  GET  /api/messages        - Get public messages')
    print('  GET  /api/messages/private - Get private messages')
    print('  POST /api/messages        - Send message')
    print('  GET  /api/users           - Get users')
    print('  POST /api/users           - Register user')
    print('  GET  /api/stats           - Statistics')
    print('')
    logger.info("Server started on port 5004")
    app.run(host='0.0.0.0', port=5004, debug=False)