from flask import Flask, request, jsonify
from datetime import datetime
import hashlib
import os

app = Flask(__name__)

# Database đơn giản
users_db = {}
likes_db = {}

@app.route('/')
def home():
    return """
    <h1>🌐 FREE FIRE API</h1>
    <p><b>📌 Cách dùng:</b></p>
    <ul>
        <li><b>GET /create?uid=123</b> - Tạo key mới</li>
        <li><b>GET /like?uid=123&key=abc</b> - Gửi like</li>
        <li><b>GET /stats?uid=123</b> - Xem stats</li>
    </ul>
    """

@app.route('/create', methods=['GET'])
def create_user():
    try:
        uid = request.args.get('uid')
        if not uid:
            return jsonify({"error": "Thiếu UID"}), 400
        
        secret = "freefire_secret_2024"
        key = hashlib.md5(f"{uid}{secret}".encode()).hexdigest()[:8]
        
        users_db[uid] = key
        likes_db[uid] = 0
        
        return jsonify({
            "success": True,
            "uid": uid,
            "key": key,
            "message": "Tạo key thành công!"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/like', methods=['GET'])
def like_user():
    try:
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
            "message": "Like thành công! 👍"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        uid = request.args.get('uid')
        if not uid:
            return jsonify({"error": "Thiếu UID"}), 400
        
        return jsonify({
            "uid": uid,
            "total_likes": likes_db.get(uid, 0),
            "status": "active",
            "server": "VN"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# QUAN TRỌNG: Đảm bảo có dòng này
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
