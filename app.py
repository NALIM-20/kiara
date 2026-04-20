import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message")
        char_name = data.get("name")
        char_bio = data.get("bio")
        api_key = os.getenv("GEMINI_KEY")

        # Opravená URL - v1beta a nový model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

        prompt = f"Hráš rolu osoby na zoznamke. Meno: {char_name}. Bio: {char_bio}. Odpovedaj krátko a slovensky na: {user_msg}"

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.9,
                "maxOutputTokens": 300
            }
        }

        response = requests.post(url, json=payload)
        result = response.json()

        print(f"DEBUG: Status kod: {response.status_code}")
        print(f"DEBUG: Odpoved od Google API: {result}")

        if 'candidates' in result:
            ai_text = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": ai_text})
        elif 'error' in result:
            error_msg = result['error'].get('message', 'Neznama chyba')
            print(f"DEBUG: Google chyba: {error_msg}")
            return jsonify({"error": "Google API error", "details": error_msg}), 400
        else:
            return jsonify({"error": "Neocakavana odpoved", "details": result}), 400

    except Exception as e:
        print(f"DEBUG CHYBA: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)