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
    # Hem "file" hem de "filename" için kontrol yap
    if "file" in request.files:
        file = request.files["file"]
    elif "filename" in request.files:
        file = request.files["filename"]
    else:
        return jsonify({"error": "No file uploaded"}), 400

    # Dosyayı işleme devam et
    content = file.read()
    # buradan sonra Gemini’ye gönderme kodun devam edecek...
    return jsonify({"answer": "Dosya alındı, boyut: {} byte".format(len(content))})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
