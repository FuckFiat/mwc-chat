#!/usr/bin/env python3
"""
Fucking Miners Chat Server
Простой сервер для синхронизации сообщений между пользователями
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Data storage
DATA_FILE = '/tmp/fucking_miners_data.json'

def load_data():
    """Load data from file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'users': {}, 'messages': []}

def save_data(data):
    """Save data to file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Initialize data
data = load_data()

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Get all messages"""
    return jsonify(data['messages'][-100:])  # Last 100 messages

@app.route('/api/messages', methods=['POST'])
def add_message():
    """Add a new message"""
    content = request.json
    message = {
        'user': content.get('user'),
        'text': content.get('text'),
        'time': content.get('time', int(datetime.now().timestamp() * 1000))
    }
    
    if not message['user'] or not message['text']:
        return jsonify({'error': 'Missing user or text'}), 400
    
    data['messages'].append(message)
    save_data(data)
    
    return jsonify({'success': True, 'message': message})

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    return jsonify(data['users'])

@app.route('/api/users/<username>', methods=['GET'])
def get_user(username):
    """Get user by name"""
    user = data['users'].get(username)
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
    if username in data['users']:
        existing = data['users'][username]
        user_data['createdAt'] = existing.get('createdAt', user_data['createdAt'])
        user_data['messageCount'] = existing.get('messageCount', 0)
    
    data['users'][username] = user_data
    save_data(data)
    
    return jsonify({'success': True, 'user': user_data})

@app.route('/api/users/<username>/online', methods=['POST'])
def set_online(username):
    """Set user online status"""
    content = request.json
    online = content.get('online', True)
    
    if username in data['users']:
        data['users'][username]['online'] = online
        data['users'][username]['lastSeen'] = int(datetime.now().timestamp() * 1000)
        save_data(data)
        return jsonify({'success': True})
    
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get chat statistics"""
    total_users = len(data['users'])
    online_users = sum(1 for u in data['users'].values() if u.get('online'))
    total_messages = len(data['messages'])
    
    return jsonify({
        'totalUsers': total_users,
        'onlineUsers': online_users,
        'totalMessages': total_messages
    })

@app.route('/api/clear', methods=['POST'])
def clear_messages():
    """Clear all messages"""
    data['messages'] = []
    save_data(data)
    return jsonify({'success': True})

if __name__ == '__main__':
    print('=== Fucking Miners Chat Server ===')
    print('Running on http://localhost:5004')
    print('API endpoints:')
    print('  GET  /api/messages - Get all messages')
    print('  POST /api/messages - Add message')
    print('  GET  /api/users - Get all users')
    print('  POST /api/users - Register user')
    print('  GET  /api/stats - Get statistics')
    print('')
    app.run(host='0.0.0.0', port=5004, debug=False)