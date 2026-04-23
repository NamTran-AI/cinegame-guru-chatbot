import os
import sys
import time
import datetime  # Thêm thư viện này để lấy thời gian thực
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

knowledge_content = load_knowledge()

# 3. Cập nhật System Instruction (Đồng bộ hoàn toàn với app.py)
current_time = datetime.datetime.now()
date_str = current_time.strftime("%d/%m/%Y")

system_instruction = (
    f"Hôm nay là ngày {date_str}. Bạn là CineGame Guru - Chuyên gia phân tích Game và Điện ảnh.\n"
    "NGUYÊN TẮC PHỤC VỤ:\n"
    "1. THÍCH NGHI: Luôn bám sát vào 'vibe' và yêu cầu cụ thể của người dùng. "
    "Nếu họ muốn tìm sự tàn bạo, hãy đưa ra gợi ý hắc ám. Nếu họ muốn sự tươi sáng, hãy gợi ý những thứ tích cực.\n"
    "2. TÍNH KẾ THỪA THÔNG MINH: Kết hợp các tiêu chuẩn ở câu hỏi trước (như đồ họa, phong cách) vào câu hỏi hiện tại, "
    "nhưng phải biết ưu tiên yêu cầu mới nhất của người dùng.\n"
    "3. ĐA DẠNG: Luôn cung cấp danh sách ít nhất 3-5 lựa chọn để người dùng có nhiều sự tham khảo.\n"
    "4. CẬP NHẬT THỜI GIAN THỰC: Dùng Google Search để kiểm tra thông tin phát hành chính xác theo ngày hiện tại.\n"
    "5. CHI TIẾT & CHUYÊN NGHIỆP: Trình bày đẹp bằng Markdown, bao gồm thông tin về Đạo diễn/NSX, Cốt truyện và các bí mật (Easter Eggs).\n\n"
    f"KHO TRI THỨC NỘI BỘ: {knowledge_content}"
)

# 4. Cơ chế Fallback và Chat logic
chat_history = []

def call_gemini_smart(history):
    # Sắp xếp lại thứ tự: Lite và Stable lên trước để tránh lỗi 429 tối đa
    candidate_models = [
        "gemini-2.0-flash-lite",
        "gemini-flash-lite-latest",
        "gemini-flash-latest",
        "gemini-2.0-flash",
        "gemini-2.5-flash"
    ]
    
    last_error = None
    for model_name in candidate_models:
        try:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[{"google_search": {}}]
            )
            response = client.models.generate_content(
                model=model_name,
                contents=history,
                config=config
            )
            return response, model_name
        except Exception as e:
            last_error = e
            # Nếu hết quota, đợi 1 giây rồi đổi model ngay
            if "429" in str(e):
                print(f"⚠️ Model {model_name} đang bận, đang chuyển sang model dự phòng...")
                time.sleep(1)
                continue
            else:
                break
    raise last_error

def main():
    print(f"--- 🎮 CineGame Guru AI (Sync Mode {date_str}) ---")
    print("Guru đã sẵn sàng! Gõ 'exit' để thoát.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "thoát"]:
            break

        chat_history.append({"role": "user", "parts": [{"text": user_input}]})
        recent_history = chat_history[-6:] # Tiết kiệm token để tránh lỗi 429

        try:
            response, used_model = call_gemini_smart(recent_history)
            chat_history.append({"role": "model", "parts": [{"text": response.text}]})
            
            print(f"\nGuru [{used_model}]:\n{response.text}")
            
            if response.candidates[0].grounding_metadata and response.candidates[0].grounding_metadata.search_entry_point:
                print("\n🌐 [Nguồn: Google Search thực tế]")
            
            print("-" * 30)

        except Exception as e:
            print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()