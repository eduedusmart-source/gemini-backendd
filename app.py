from flask import Flask, request
import google.generativeai as genai
import os

app = Flask(__name__)

# 🔑 Gemini API Key (Render üzerinde Environment Variables kısmına eklenecek)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

@app.route("/")
def home():
    return "✅ Gemini Backend Çalışıyor!"

# 📝 Metin çözümleme
@app.route("/solve_text", methods=["POST"])
def solve_text():
    # Gönderilen text'i al
    question = request.data.decode("utf-8").strip()

    if not question:
        return "⚠️ Soru boş olamaz", 400

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(question)

    return response.text  # ✅ düz metin döner

# 🖼️ Resim çözümleme
@app.route("/solve_image", methods=["POST"])
def solve_image():
    if "file" not in request.files:
        return "⚠️ Fotoğraf gönderilmedi", 400

    file = request.files["file"]
    content = file.read()

    # Şimdilik test için sadece boyut döndürüyoruz
    return f"📷 Fotoğraf alındı, boyut: {len(content)} byte"

if __name__ == "__main__":
    # Render kendi portunu ENV değişkeninde verir
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
