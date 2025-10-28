from flask import Flask, render_template, jsonify
import os
import socket
import redis
import datetime

app = Flask(__name__)

# Подключение к Redis
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'hostname': socket.gethostname()
    })

@app.route('/api/visits', methods=['GET', 'POST'])
def visits():
    if redis_client:
        try:
            count = redis_client.incr('visit_count')
            return jsonify({
                'visit_count': count,
                'message': f'Это посещение номер {count}'
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Redis not available'}), 503

@app.route('/api/info')
def info():
    return jsonify({
        'app_name': 'My K8s App',
        'version': '1.0.0',
        'environment': os.environ.get('ENVIRONMENT', 'development'),
        'redis_host': redis_host,
        'redis_port': redis_port
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
