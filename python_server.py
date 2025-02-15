from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
users = set()  # Registered users
messages = {}  # Stores messages {recipient: [{"from": sender, "content": message}, ...]}

@app.route('/register', methods=['POST'])
def register():
    user_id = request.headers.get('UserId')
    if not user_id:
        return jsonify({"error": "UserId header is required"}), 400
    
    users.add(user_id)
    messages.setdefault(user_id, [])  # Initialize empty message list for the user
    return jsonify({"message": f"User {user_id} registered successfully"}), 201

@app.route('/message/send', methods=['POST'])
def send_message():
    user_id = request.headers.get('UserId')
    data = request.get_json()

    if not user_id or not data or "to" not in data or "content" not in data:
        return jsonify({"error": "Invalid request"}), 400

    recipient = data["to"]
    if recipient not in users:
        return jsonify({"error": "Recipient not registered"}), 404

    # Store message
    messages[recipient].append({"from": user_id, "content": data["content"]})
    return jsonify({"message": "Message sent successfully"}), 200

@app.route('/message/poll', methods=['GET'])
def poll_messages():
    user_id = request.headers.get('UserId')
    if not user_id or user_id not in users:
        return jsonify({"error": "User not registered"}), 404

    user_messages = messages.get(user_id, [])
    messages[user_id] = []  # Clear messages after polling
    return jsonify(user_messages), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
