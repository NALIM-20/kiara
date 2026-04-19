import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# CORS umožňuje tvojmu webu (Frontend) komunikovať s týmto serverom (Backend)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get("message")
    char_name = data.get("name")
    char_bio = data.get("bio")

    # Premennú GEMINI_KEY nastavíme priamo v ovládacom paneli na Renderi
    api_key = os.getenv("GEMINI_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    # Tu povieme AI, ako sa má správať (System Instruction)
    prompt = f"Hráš rolu osoby na zoznamke. Tvoje meno: {char_name}. Tvoje bio: {char_bio}. Odpovedaj krátko, vtipne a slovensky na správu: {user_msg}"
    
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        # Vytiahneme text odpovede z výsledku od Googlu
        ai_text = result['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"reply": ai_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Port sa nastaví automaticky podľa prostredia Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)