from flask import Flask, request, jsonify
import openai
from flask_cors import CORS  # Import CORS to handle cross-origin requests

app = Flask(__name__)

# Enable CORS for your frontend (this allows requests from http://127.0.0.1:5500)
CORS(app, resources={r"/ask": {"origins": "http://127.0.0.1:5500"}})  # Adjust this if your frontend runs on a different port

# Your OpenAI API key
openai.api_key = '#Your Api key '

# Basic route for the home page
@app.route('/')
def home():
    return "Welcome to the Space Bot! Ask me anything about space."

# Route to interact with the chatbot
@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('question')
    
    if not user_input:
        return jsonify({'error': 'Please provide a question.'}), 400

    try:
        # Correct usage for OpenAI API >= 1.0.0
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can replace with your fine-tuned model if needed
            messages=[
                {"role": "user", "content": user_input}
            ],
            max_tokens=100
        )
        
        # Extracting the answer from the response
        answer = response['choices'][0]['message']['content'].strip()
        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
