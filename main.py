import os
from google import genai
from dotenv import load_dotenv

# 1. Tải các biến môi trường từ file .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# 2. Hàm đọc dữ liệu từ file kienthuc.txt
def doc_du_lieu_rag(file_path):
    try:
        # Sử dụng encoding="utf-8" để đọc được tiếng Việt và các ký tự đặc biệt
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Lỗi khi đọc file kiến thức: {e}")
        return ""

# Nạp dữ liệu Easter Eggs vào biến
du_lieu_gta = doc_du_lieu_rag("kienthuc.txt")

# 3. Định nghĩa Persona kết hợp Dữ liệu từ file (RAG)
huong_dan_he_thong = f"""
Bạn là 'CineGame Guru' - chuyên gia hàng đầu về điện ảnh và trò chơi điện tử.
Phong cách: Nhiệt huyết, am hiểu sâu sắc, hay sử dụng thuật ngữ chuyên môn.

Dưới đây là KHO DỮ LIỆU BÍ MẬT (Easter Eggs) bạn phải dùng để trả lời:
---
{du_lieu_gta}
---

Nhiệm vụ:
- Nếu người dùng hỏi về các bí ẩn, hồn ma, hoặc UFO trong GTA, hãy dùng dữ liệu trên.
- Trả lời chi tiết và dẫn dắt người dùng như một chuyên gia thực thụ.
"""

# 4. Khởi tạo Chat với Model
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={'system_instruction': huong_dan_he_thong}
)

print("--- 🎮 CINEGAME GURU: RAG EDITION ĐÃ SẴN SÀNG ---")

while True:
    user_input = input("Bạn: ")
    if user_input.lower() in ["thoát", "exit", "nghỉ"]: 
        break
        
    try:
        response = chat.send_message(user_input)
        print(f"Guru: {response.text}")
    except Exception as e:
        print(f"Lỗi: {e}")