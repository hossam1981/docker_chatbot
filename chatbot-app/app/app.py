from flask import Flask, request, jsonify
import redis
from pymongo import MongoClient
import requests

app = Flask(__name__)

# Redis setup
r = redis.Redis(host='redis', port=6379, db=0)

# MongoDB setup
client = MongoClient('mongodb://mongo:27017/')
db = client.chatbot
messages = db.messages

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    # Check cache
    cached = r.get(user_input)
    if cached:
        return jsonify({"response": cached.decode()})

    # Call LLaMA API
    llama_response = requests.post("http://llama:8000/generate", json={"prompt": user_input})
    response = llama_response.json().get("response")

    # Cache and store
    r.set(user_input, response)
    messages.insert_one({"user": user_input, "bot": response})

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)