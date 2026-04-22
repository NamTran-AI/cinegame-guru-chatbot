import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

print("--- DANH SÁCH MODELS BẠN CÓ THỂ DÙNG ---")

try:
    # Lấy danh sách model một cách đơn giản nhất
    for model in client.models.list():
        print(f"Tên Model: {model.name}")
except Exception as e:
    print(f"Lỗi: {e}")