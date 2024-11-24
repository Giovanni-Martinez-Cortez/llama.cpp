from flask import Flask, jsonify, request
from flask_cors import CORS
from llama_cpp import Llama
from waitress import serve

llm = Llama(
    model_path="./models/llama-3.2-1b-instruct-q8_0.gguf",
)

app = Flask(__name__)
CORS(app)

@app.route("/processprompt", methods=['POST'])
def processPrompt():
    input = request.json['prompt']  # Ensure that this key exists in the request
    output = llm.create_chat_completion(
        messages = [
            {"role": "system", "content": "You are an online assistant who answers questions and have a formal conversation with anyone."},
            {"role": "user", "content": input}
        ]
    )
    response = jsonify({'text': output['choices'][0]['message']['content']})  # Ensure you're extracting the text from output
    return response

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
