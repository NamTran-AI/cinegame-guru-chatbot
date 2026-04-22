import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Tải cấu hình
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ Lỗi: Không tìm thấy GEMINI_API_KEY")
    sys.exit()

client = genai.Client(api_key=API_KEY)

# 2. Đọc dữ liệu từ knowledge.txt
def load_knowledge():
    file_path = "knowledge.txt"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

knowledge_data = load_knowledge()

# 3. System Instruction mạnh mẽ hơn
system_prompt = f"""
Bạn là 'CineGame Guru', chuyên gia giải trí hàng đầu. 
Hôm nay là Thứ Tư, ngày 22 tháng 04 năm 2026.

DỮ LIỆU NỘI BỘ:
---
{knowledge_data}
---

QUY TẮC TRẢ LỜI:
1. Luôn kiểm tra DỮ LIỆU NỘI BỘ trước.
2. Nếu dữ liệu nội bộ cũ hoặc không có, BẮT BUỘC dùng Google Search để lấy tin tức mới nhất của năm 2026.
3. Nếu thông tin trong file và Google Search mâu thuẫn, hãy ưu tiên thông tin mới nhất từ Google Search và giải thích ngắn gọn.
4. Trả lời phong cách chuyên gia, hài hước, dùng thuật ngữ game thủ.
"""

# 4. Khởi tạo phiên Chat với cấu hình chuẩn
chat = client.chats.create(
    model="gemini-2.5-flash", # Đổi sang 2.0 để ổn định hơn
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[{"google_search": {}}]
    )
)

def main():
    print("--- 🎮 CineGame Guru AI (Grounding Mode 2026) ---")
    print("Guru đã sẵn sàng! Gõ 'exit' để thoát.")
    print(f"Dữ liệu nội bộ: {len(knowledge_data)} ký tự.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "thoát"]:
            break

        try:
            response = chat.send_message(user_input)
            
            print(f"\nGuru: {response.text}")
            
            # Kiểm tra nguồn Search
            if response.candidates[0].grounding_metadata and response.candidates[0].grounding_metadata.search_entry_point:
                print("\n🌐 [Nguồn: Đã được cập nhật từ Google Search thực tế]")
            
            print("-" * 30)

        except Exception as e:
            print(f"❌ Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    main()