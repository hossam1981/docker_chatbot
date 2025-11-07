from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the OpenAI client
# The API key is automatically read from the OPENAI_API_KEY environment variable
try:
    client = OpenAI()
    api_key_present = os.getenv("OPENAI_API_KEY") is not None
    if not api_key_present:
        logging.warning("OPENAI_API_KEY environment variable not found.")
except Exception as e:
    client = None
    logging.error(f"Error initializing OpenAI client: {e}")


@app.route("/generate", methods=["POST"])
def generate():
    if not client or not api_key_present:
        error_msg = "OpenAI API key is missing or the client is not initialized."
        logging.error(error_msg)
        return jsonify({"error": error_msg}), 500

    prompt = request.json.get("prompt")
    if not prompt:
        logging.warning("Prompt is missing from the request.")
        return jsonify({"error": "Prompt is missing from the request."}), 400

    try:
        logging.info(f"Received prompt: {prompt}")
        # Create a chat completion call to OpenAI
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
            max_tokens=150,
        )
        response = chat_completion.choices[0].message.content
        logging.info(f"Generated response: {response}")
        return jsonify({"response": response})

    except Exception as e:
        logging.error(f"An error occurred while calling OpenAI API: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)