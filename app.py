from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from instagrapi import Client
import os
import random
import sqlite3
from datetime import datetime, timedelta
import requests
import base64
import pytz

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Config
DASHBOARD_PASSWORD = os.getenv('DASHBOARD_PASSWORD', 'htybrertf:;:45635879cd!')
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME', 'kungfu.painda')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD', 'htybrertf:;:45635879c')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
IMAGES_DIR = 'images'
DB_FILE = 'posts.db'
SESSION_FILE = 'instagram_session.json'

# Global Instagram client
instagram_client = None

def require_auth(f):
    def wrapper(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def get_instagram_client():
    global instagram_client
    if instagram_client:
        return instagram_client
    
    cl = Client()
    cl.delay_range = [1, 3]
    
    # Try to load existing session
    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            instagram_client = cl
            print("Loaded existing Instagram session")
            return cl
        except Exception as e:
            print(f"Failed to load session: {e}")
            os.remove(SESSION_FILE)
    
    # Fresh login
    try:
        cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        cl.dump_settings(SESSION_FILE)
        instagram_client = cl
        print("Created new Instagram session")
        return cl
    except Exception as e:
        raise Exception(f"Instagram login failed: {str(e)}")

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
    c.execute('''CREATE TABLE IF NOT EXISTS scheduled_posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  scheduled_time TEXT,
                  is_recurring INTEGER DEFAULT 0,
                  is_active INTEGER DEFAULT 1,
                  created_at TEXT)''')
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
    image_path = None
    try:
        image_path = get_random_image()
        if not image_path:
            return {'success': False, 'error': 'No images found'}
        
        print(f"Selected image: {image_path}")
        caption = generate_caption(image_path)
        print(f"Generated caption: {caption[:50]}...")
        
        print("Getting Instagram client...")
        cl = get_instagram_client()
        print("Uploading photo...")
        cl.photo_upload(image_path, caption)
        print("Photo uploaded successfully!")
        
        # Save to database
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT INTO posts (image_path, caption, timestamp, status) VALUES (?, ?, ?, ?)',
                  (image_path, caption, datetime.now().isoformat(), 'success'))
        conn.commit()
        conn.close()
        
        return {'success': True, 'image': image_path, 'caption': caption}
    except Exception as e:
        error_msg = str(e)
        print(f"Error posting to Instagram: {error_msg}")
        import traceback
        traceback.print_exc()
        
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT INTO posts (image_path, caption, timestamp, status) VALUES (?, ?, ?, ?)',
                  (image_path or 'unknown', error_msg, datetime.now().isoformat(), 'failed'))
        conn.commit()
        conn.close()
        return {'success': False, 'error': error_msg}

# Scheduler
scheduler = BackgroundScheduler()

def load_scheduled_jobs():
    """Load all active scheduled posts from database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, scheduled_time, is_recurring FROM scheduled_posts WHERE is_active = 1')
    schedules = c.fetchall()
    conn.close()
    
    # Clear existing jobs
    scheduler.remove_all_jobs()
    
    # Add jobs from database
    for schedule_id, scheduled_time, is_recurring in schedules:
        dt = datetime.fromisoformat(scheduled_time)
        # Make timezone aware if naive
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=pytz.UTC)
        
        if is_recurring:
            # Daily recurring job
            scheduler.add_job(
                post_to_instagram,
                'cron',
                hour=dt.hour,
                minute=dt.minute,
                id=f'recurring_{schedule_id}'
            )
        else:
            # One-time job
            now = datetime.now(pytz.UTC)
            if dt > now:
                scheduler.add_job(
                    post_to_instagram,
                    'date',
                    run_date=dt,
                    id=f'onetime_{schedule_id}'
                )

# Initialize with default 5 AM schedule
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM scheduled_posts WHERE is_recurring = 1')
if c.fetchone()[0] == 0:
    c.execute('INSERT INTO scheduled_posts (scheduled_time, is_recurring, created_at) VALUES (?, 1, ?)',
              (datetime.now().replace(hour=5, minute=0, second=0).isoformat(), datetime.now().isoformat()))
    conn.commit()
conn.close()

load_scheduled_jobs()
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/auth', methods=['POST'])
def auth():
    password = request.json.get('password')
    if password == DASHBOARD_PASSWORD:
        session['authenticated'] = True
        return jsonify({'success': True})
    return jsonify({'success': False}), 401

@app.route('/api/status')
@require_auth
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
@require_auth
def trigger():
    result = post_to_instagram()
    return jsonify(result)

@app.route('/api/history')
@require_auth
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

@app.route('/api/schedules')
@require_auth
def get_schedules():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM scheduled_posts WHERE is_active = 1 ORDER BY scheduled_time')
    schedules = c.fetchall()
    conn.close()
    
    return jsonify([{
        'id': s[0],
        'scheduled_time': s[1],
        'is_recurring': bool(s[2]),
        'created_at': s[4]
    } for s in schedules])

@app.route('/api/schedule', methods=['POST'])
@require_auth
def add_schedule():
    data = request.json
    scheduled_time = data.get('scheduled_time')
    is_recurring = data.get('is_recurring', False)
    
    try:
        dt = datetime.fromisoformat(scheduled_time)
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT INTO scheduled_posts (scheduled_time, is_recurring, created_at) VALUES (?, ?, ?)',
                  (scheduled_time, 1 if is_recurring else 0, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        load_scheduled_jobs()
        return jsonify({'success': True, 'message': 'Schedule added'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/schedule/<int:schedule_id>', methods=['DELETE'])
@require_auth
def delete_schedule(schedule_id):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('UPDATE scheduled_posts SET is_active = 0 WHERE id = ?', (schedule_id,))
        conn.commit()
        conn.close()
        
        load_scheduled_jobs()
        return jsonify({'success': True, 'message': 'Schedule removed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
