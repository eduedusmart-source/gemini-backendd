from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# 🔑 Gemini API Key Render üzerinde Environment Variables kısmına eklenecek
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

@app.route("/")
def home():
    return "✅ Gemini Backend Çalışıyor!"

@app.route("/solve_text", methods=["POST"])
def solve_text():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "Soru boş olamaz"}), 400

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(question)

    return jsonify({"answer": response.text})

@app.route("/solve_image", methods=["POST"])
def solve_image():
    if "file" not in request.files:
        return jsonify({"error": "Resim bulunamadı"}), 400

    file = request.files["file"]
    img_bytes = file.read()

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([
        "Bu görseldeki soruyu çöz ve adım adım açıkla.",
        {"mime_type": "image/jpeg", "data": img_bytes}
    ])

    return jsonify({"answer": response.text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
