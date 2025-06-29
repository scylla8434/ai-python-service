from flask import Flask, request, jsonify
import cohere
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
co = cohere.Client(os.environ.get("COHERE_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    response = co.generate(
        model='command',
        prompt=question,
        max_tokens=256
    )
    return jsonify({'answer': response.generations[0].text.strip()})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
