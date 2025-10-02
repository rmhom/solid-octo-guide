
import os
from datetime import datetime
from flask import Flask, send_from_directory

app = Flask(__name__)

# 提供静态HTML文件
@app.route('/')
def home():
    return send_from_directory('.', 'live_scroll.html')

@app.route('/live_scroll.html')
def live_scroll():
    return send_from_directory('.', 'live_scroll.html')

@app.route('/live_dashboard.html')
def live_dashboard():
    return send_from_directory('.', 'live_dashboard.html')

@app.route('/health')
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# 提供其他静态文件
@app.route('/<path:filename>')
def static_files(filename):
    if os.path.exists(filename):
        return send_from_directory('.', filename)
    return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
