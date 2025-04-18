import os
from g4f.client import Client
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
client = Client()

port = int(os.getenv("PORT", 3001))
CORS(app)

@app.route('/', methods=['GET'])
def getMain():
    return 'g4f-proxy is running'

@app.route('/', methods=['POST'])
def postG4F():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # Required attributes
    required_fields = ["system", "user"]

    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": data['system']},
            {"role": "user", "content": data['user']}
        ],
        web_search=False
    )
    
    return response.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True, port=port)