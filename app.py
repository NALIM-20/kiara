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
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

        prompt = f"Hráš rolu osoby na zoznamke. Meno: {char_name}. Bio: {char_bio}. Odpovedaj krátko a slovensky na: {user_msg}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        response = requests.post(url, json=payload)
        result = response.json()

        # TENTO RIADOK NÁM POMÔŽE: Vypíše odpoveď od Googlu do logov na Renderi
        print(f"DEBUG: Odpoved od Google API: {result}")

        if 'candidates' in result:
            ai_text = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": ai_text})
        else:
            # Ak Google vráti chybu (napr. neplatný kľúč), pošleme ju do logov
            return jsonify({"error": "Google API error", "details": result}), 400

    except Exception as e:
        print(f"DEBUG CHYBA: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)