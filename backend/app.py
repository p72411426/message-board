from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_FILE = 'messages.db'

# --- 初始化数据库 ---
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# --- 获取数据库连接 ---
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = lambda cursor, row: row[0]  # 只返回内容
    return conn

# --- 首页：显示欢迎信息 ---
@app.route('/')
def index():
    return '''
        <h1>🎉 Flask 后端已成功部署！</h1>
        <p>欢迎使用留言板 API</p>
        <p>GET/POST 留言请访问：<code>/messages</code></p>
    '''

# --- 获取留言列表 ---
@app.route('/messages', methods=['GET'])
def get_messages():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # 让结果可以当作字典读取
    messages = conn.execute('SELECT username, content FROM messages ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(m) for m in messages])

# --- 添加新留言 ---
@app.route('/messages', methods=['POST'])
def post_message():
    data = request.json
    username = data.get('username')
    message = data.get('message')
    if username and message:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO messages (username, content) VALUES (?, ?)',
            (username, message)
        )
        conn.commit()
        conn.close()
        return jsonify({'status': 'ok'}), 201
    else:
        return jsonify({'error': 'Missing username or message'}), 400

# --- 程序入口 ---
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5001))  # 从环境变量读取 PORT，默认是 5001（本地测试用）
    app.run(host='0.0.0.0', port=port)
