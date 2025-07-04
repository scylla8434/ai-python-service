from flask import Flask, request, jsonify
import cohere
import os
import threading
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
co = cohere.Client(os.environ.get("COHERE_API_KEY"))

# Global variable to track service health
last_activity = datetime.now()

def update_activity():
    """Update the last activity timestamp"""
    global last_activity
    last_activity = datetime.now()

@app.route('/chat', methods=['POST'])
def chat():
    update_activity()
    try:
        data = request.json
        question = data.get('question')
        if not question:
            return jsonify({'error': 'No question provided'}), 400
            
        response = co.generate(
            model='command',
            prompt=question,
            max_tokens=256
        )
        return jsonify({'answer': response.generations[0].text.strip()})
    except Exception as e:
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500

@app.route('/')
def home():
    update_activity()
    return 'AI Python Service is running!', 200

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    update_activity()
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'last_activity': last_activity.isoformat(),
        'service': 'ai-python-service'
    }), 200

@app.route('/ping')
def ping():
    """Simple ping endpoint"""
    update_activity()
    return jsonify({'pong': True, 'timestamp': datetime.now().isoformat()}), 200

def self_ping():
    """Self-ping function to keep the service alive"""
    service_url = os.environ.get('SERVICE_URL', 'https://ai-python-service.onrender.com')
    
    while True:
        try:
            # Wait 14 minutes (840 seconds) between pings
            # Render free tier sleeps after 15 minutes of inactivity
            time.sleep(840)
            
            # Ping the health endpoint
            response = requests.get(f"{service_url}/health", timeout=30)
            
            if response.status_code == 200:
                print(f"✅ Keepalive ping successful at {datetime.now()}")
            else:
                print(f"⚠️ Keepalive ping returned status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Keepalive ping failed: {str(e)}")

def start_keepalive():
    """Start the keepalive thread"""
    # Only start keepalive in production (when deployed on Render)
    if os.environ.get('RENDER'):
        keepalive_thread = threading.Thread(target=self_ping, daemon=True)
        keepalive_thread.start()
        print("🔄 Keepalive thread started")

if __name__ == '__main__':
    app.run(port=5001, debug=True)
else:
    # Start keepalive when running with gunicorn
    start_keepalive()