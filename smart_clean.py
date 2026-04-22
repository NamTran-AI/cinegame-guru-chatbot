import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def smart_cleanup():
    file_path = "knowledge.txt"
    if not os.path.exists(file_path):
        print("❌ Không tìm thấy file knowledge.txt")
        return

    # 1. Đọc nội dung hiện tại
    with open(file_path, "r", encoding="utf-8") as f:
        old_content = f.read()

    print("🧠 Guru đang xem xét và dọn dẹp dữ liệu cho bạn...")

    # 2. Gửi yêu cầu cho Gemini lọc dữ liệu
    prompt = f"""
    Below is my AI chatbot's knowledge base. Please:
    1. Remove duplicated information.
    2. Remove outdated or contradictory facts.
    3. Keep the information concise and well-organized.
    4. Return ONLY the cleaned text, do not add any comments.

    CONTENT:
    {old_content}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    new_content = response.text

    # 3. Cho bạn xem thử trước khi lưu
    print("\n--- NỘI DUNG ĐÃ ĐƯỢC AI DỌN DẸP ---")
    print(new_content[:500] + "...") # Hiển thị 500 ký tự đầu
    
    confirm = input("\n⚠️ Bạn có muốn lưu bản này đè lên knowledge.txt không? (y/n): ")
    
    if confirm.lower() == 'y':
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ Đã cập nhật kiến thức sạch!")
    else:
        print("❌ Đã hủy bỏ thay đổi.")

if __name__ == "__main__":
    smart_cleanup()