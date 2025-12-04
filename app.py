from flask import Flask, render_template, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from instagrapi import Client
import os
import random
import sqlite3
from datetime import datetime, timedelta
import requests
import base64

app = Flask(__name__)

# Config
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME', 'kungfu.painda')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD', 'htybrertf:;:45635879c')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
IMAGES_DIR = 'images'
DB_FILE = 'posts.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  image_path TEXT,
                  caption TEXT,
                  timestamp TEXT,
                  status TEXT)''')
    conn.commit()
    conn.close()

init_db()

def get_random_image():
    all_images = []
    for root, dirs, files in os.walk(IMAGES_DIR):
        for f in files:
            if f.endswith(('.jpg', '.jpeg', '.png')):
                all_images.append(os.path.join(root, f))
    return random.choice(all_images) if all_images else None

def generate_caption(image_path):
    if not OPENAI_API_KEY:
        return "Embrace your inner warrior 🐼💪 #KungFuPanda #Wisdom #Motivation"
    
    try:
        with open(image_path, 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode()
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
            json={
                'model': 'gpt-4o',
                'messages': [{
                    'role': 'system',
                    'content': 'Analyze image and output JSON: {"caption":"50-100 words with emojis","hashtags":["15-20 tags no #"]}'
                }, {
                    'role': 'user',
                    'content': [{
                        'type': 'text',
                        'text': 'Analyze Kung Fu Panda image, generate matching wisdom caption'
                    }, {
                        'type': 'image_url',
                        'image_url': {'url': f'data:image/jpeg;base64,{image_base64}'}
                    }]
                }],
                'temperature': 0.9,
                'max_tokens': 500
            }
        )
        
        content = response.json()['choices'][0]['message']['content']
        import json
        data = json.loads(content.replace('```json', '').replace('```', '').strip())
        hashtags = ' '.join([f"#{tag}" for tag in data['hashtags']])
        return f"{data['caption']}\n\n{hashtags}"
    except:
        return "Embrace your inner warrior 🐼💪 #KungFuPanda #Wisdom #Motivation"

def post_to_instagram():
    try:
        image_path = get_random_image()
        if not image_path:
            return {'success': False, 'error': 'No images found'}
        
        caption = generate_caption(image_path)
        
        cl = Client()
        cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        cl.photo_upload(image_path, caption)
        
        # Save to database
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT INTO posts (image_path, caption, timestamp, status) VALUES (?, ?, ?, ?)',
                  (image_path, caption, datetime.now().isoformat(), 'success'))
        conn.commit()
        conn.close()
        
        return {'success': True, 'image': image_path, 'caption': caption}
    except Exception as e:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT INTO posts (image_path, caption, timestamp, status) VALUES (?, ?, ?, ?)',
                  (image_path if 'image_path' in locals() else '', str(e), datetime.now().isoformat(), 'failed'))
        conn.commit()
        conn.close()
        return {'success': False, 'error': str(e)}

# Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(post_to_instagram, 'cron', hour=5, minute=0)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    # Get next scheduled time
    next_run = scheduler.get_jobs()[0].next_run_time if scheduler.get_jobs() else None
    
    # Get last post
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM posts ORDER BY id DESC LIMIT 1')
    last_post = c.fetchone()
    conn.close()
    
    return jsonify({
        'next_post': next_run.isoformat() if next_run else None,
        'last_post': {
            'image': last_post[1],
            'caption': last_post[2],
            'timestamp': last_post[3],
            'status': last_post[4]
        } if last_post else None,
        'service_status': 'running'
    })

@app.route('/api/trigger', methods=['POST'])
def trigger():
    result = post_to_instagram()
    return jsonify(result)

@app.route('/api/history')
def history():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM posts ORDER BY id DESC LIMIT 10')
    posts = c.fetchall()
    conn.close()
    
    return jsonify([{
        'id': p[0],
        'image': p[1],
        'caption': p[2],
        'timestamp': p[3],
        'status': p[4]
    } for p in posts])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
