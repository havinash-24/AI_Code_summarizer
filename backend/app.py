from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from main import run_pipeline

# Load API keys from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/generate-doc', methods=['POST'])
def generate_doc():
    try:
        data = request.get_json()
        print("✅ Received request data:", data)

        code_snippet = data.get('code')
        if not code_snippet:
            print("⚠️ No code provided in request.")
            return jsonify({"error": "No code snippet provided."}), 400

        # Run main agent pipeline
        result = run_pipeline(code_snippet)
        print("✅ Pipeline result:", result)

        return jsonify(result), 200

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
