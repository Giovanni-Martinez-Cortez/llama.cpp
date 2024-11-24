import os
from google.cloud import storage
from flask import Flask, jsonify, request
from flask_cors import CORS
from llama_cpp import Llama
from waitress import serve

# Function to download model from Cloud Storage
def download_model_from_gcs(bucket_name, model_path, local_model_path):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(model_path)
    blob.download_to_filename(local_model_path)

# Cloud Storage bucket and model path
bucket_name = 'your-bucket-name'
cloud_model_path = 'models/llama-3.2-1b-instruct-q8_0.gguf'
local_model_path = './models/llama-3.2-1b-instruct-q8_0.gguf'

# Check if the model exists locally, otherwise download from Cloud Storage
if not os.path.exists(local_model_path):
    download_model_from_gcs(bucket_name, cloud_model_path, local_model_path)

# Load the model
llm = Llama(model_path=local_model_path)

app = Flask(__name__)
CORS(app)

@app.route("/processprompt", methods=['POST'])
def processPrompt():
    input = request.json['prompt']  # Ensure that this key exists in the request
    output = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "You are an online assistant who answers questions and has a formal conversation with anyone."},
            {"role": "user", "content": input}
        ]
    )
    response = jsonify({'text': output['choices'][0]['message']['content']})  # Ensure you're extracting the text from output
    return response

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
