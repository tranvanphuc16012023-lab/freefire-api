from flask import Flask, request, jsonify
from datetime import datetime
import hashlib

app = Flask(__name__)

# Database đơn giản
users_db = {}
likes_db = {}

@app.route('/')
def home():
    return """
    <h1>🌐 FREE FIRE API CỦA BẠN</h1>
    <p><b>📌 Cách dùng:</b></p>
    <ul>
        <li><b>GET /create?uid=123</b> - Tạo key mới</li>
        <li><b>GET /like?uid=123&key=abc</b> - Gửi like</li>
        <li><b>GET /stats?uid=123</b> - Xem thống kê</li>
    </ul>
    <p>🔗 <b>URL gốc:</b> https://your-api.onrender.com</p>
    """

@app.route('/create', methods=['GET'])
def create_user():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({"error": "Thiếu UID"}), 400
    
    # Tạo key từ UID
    secret = "freefire_secret_2024"
    key = hashlib.md5(f"{uid}{secret}".encode()).hexdigest()[:8]
    
    users_db[uid] = key
    likes_db[uid] = 0
    
    return jsonify({
        "success": True,
        "uid": uid,
        "key": key,
        "message": "Tạo key thành công!",
        "api_url": f"https://your-api.onrender.com/like?uid={uid}&key={key}"
    })

@app.route('/like', methods=['GET'])
def like_user():
    uid = request.args.get('uid')
    key = request.args.get('key')
    
    if not uid or not key:
        return jsonify({"error": "Thiếu UID hoặc Key"}), 400
    
    if uid not in users_db or users_db[uid] != key:
        return jsonify({"error": "Key không hợp lệ"}), 401
    
    likes_db[uid] = likes_db.get(uid, 0) + 1
    
    return jsonify({
        "success": True,
        "uid": uid,
        "total_likes": likes_db[uid],
        "timestamp": datetime.now().isoformat(),
        "message": "Like thành công! 👍"
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({"error": "Thiếu UID"}), 400
    
    return jsonify({
        "uid": uid,
        "total_likes": likes_db.get(uid, 0),
        "account_created": uid in users_db,
        "server": "VN",
        "status": "active"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)