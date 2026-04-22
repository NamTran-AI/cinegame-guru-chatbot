import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Tải cấu hình từ file .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ Lỗi: Không tìm thấy GEMINI_API_KEY trong file .env")
    sys.exit()

# 2. Khởi tạo Client
client = genai.Client(api_key=API_KEY)

# 3. Đọc dữ liệu từ knowledge.txt
def load_knowledge():
    file_path = "knowledge.txt"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        # Tạo file trống nếu chưa có để tránh lỗi
        open(file_path, "w", encoding="utf-8").close()
        return ""

knowledge_data = load_knowledge()

# 4. Thiết lập hướng dẫn hệ thống (System Instruction)
system_prompt = f"""
You are 'CineGame Guru', a professional expert in entertainment, including video games and cinema.
Your knowledge base is derived from the following provided text:
---
{knowledge_data}
---
INSTRUCTIONS:
1. Prioritize information from the provided text above.
2. If the information is not in the text, use your internal knowledge and 'Google Search' to provide accurate and up-to-date answers.
3. Always maintain a helpful, engaging, and professional tone.
4. If you use Google Search to answer, focus on reliable sources like official game wikis, IMDB, or reputable tech news.
5. Answer in the same language as the user's question.
"""

# 5. Khởi tạo phiên Chat với Google Search Grounding
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[types.Tool(google_search={})] # Kích hoạt Grounding
    )
)

def main():
    print("--- 🎮 CineGame Guru AI (Grounding Mode) ---")
    print("Guru đã sẵn sàng! Gõ 'exit' để thoát.")
    print(f"Dữ liệu nội bộ: {len(knowledge_data)} ký tự đã được nạp từ knowledge.txt.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "thoát"]:
            break

        try:
            # Gửi tin nhắn và nhận phản hồi
            response = chat.send_message(user_input)
            
            print(f"\nGuru: {response.text}")
            
            # Kiểm tra xem AI có dùng Google Search không (Grounding Metadata)
            if response.candidates[0].grounding_metadata:
                print("\n[Nguồn: Đã được xác thực qua Google Search]")
            
            print("-" * 30)

        except Exception as e:
            print(f"❌ Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    main()