import os
from dotenv import load_dotenv
from google import genai

# 1. Cấu hình ban đầu
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
FILE_PATH = "knowledge.txt"

def smart_cleanup():
    if not os.path.exists(FILE_PATH):
        print(f"❌ Không tìm thấy file {FILE_PATH}")
        return

    # 2. Đọc nội dung hiện có
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        old_content = f.read().strip()

    if not old_content:
        print("💡 File đang trống, không có gì để dọn dẹp.")
        return

    print("🧠 Guru đang xem xét và tự động dọn dẹp dữ liệu...")

    # 3. Gửi yêu cầu cho Gemini lọc dữ liệu
    prompt = f"""
    Bạn là một chuyên gia quản lý dữ liệu. Hãy giúp tôi dọn dẹp file kiến thức này:
    1. Loại bỏ các dòng thông báo lỗi (ví dụ: 'JavaScript is disabled', 'Access denied', '403 Forbidden').
    2. Loại bỏ các thông tin trùng lặp hoặc mâu thuẫn.
    3. Sắp xếp lại nội dung cho gọn gàng, súc tích.
    4. Giữ lại toàn bộ kiến thức hữu ích về phim ảnh và trò chơi.
    
    CHỈ TRẢ VỀ NỘI DUNG ĐÃ DỌN DẸP, KHÔNG THÊM BẤT KỲ LỜI GIẢI THÍCH NÀO.

    NỘI DUNG CẦN DỌN DẸP:
    {old_content}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        new_content = response.text.strip()

        # 4. Kiểm tra và tự động cập nhật
        if new_content and len(new_content) > 10:
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("✅ Đã tự động cập nhật và dọn dẹp kiến thức thành công!")
        else:
            print("⚠️ Cảnh báo: Kết quả AI trả về quá ngắn hoặc rỗng, không ghi đè để bảo vệ file.")

    except Exception as e:
        print(f"❌ Lỗi khi kết nối với AI: {e}")

if __name__ == "__main__":
    smart_cleanup()