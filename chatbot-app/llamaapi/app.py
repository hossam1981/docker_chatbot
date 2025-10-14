from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.json.get("prompt")
    response = f"LLaMA says: {prompt}"  # Replace with actual model call if needed
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)