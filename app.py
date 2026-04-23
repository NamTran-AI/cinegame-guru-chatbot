import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import time
import datetime

# 1. Tải các biến môi trường
load_dotenv()

# 2. Cấu hình trang Web
st.set_page_config(
    page_title="CineGame Guru | AI Agent", 
    page_icon="🎮", 
    layout="centered"
)

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎮 CineGame Guru AI")
st.caption("Real-time Context | Multi-Model Fallback | Dynamic Timeline")

# 3. Khởi tạo kết nối
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 4. Hàm nạp tri thức nội bộ
@st.cache_data
def get_knowledge():
    knowledge_path = "knowledge.txt"
    if os.path.exists(knowledge_path):
        with open(knowledge_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Không tìm thấy dữ liệu tri thức nội bộ."

knowledge_content = get_knowledge()

# 5. Cấu hình System Instruction (Đồng bộ hoàn toàn với main.py)
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

# 6. Hàm gọi AI thông minh (Đã cập nhật thứ tự Model chuẩn)
def call_gemini_smart(history):
    # Đội hình Gemini thuần túy - Luôn ổn định nhất với tính năng Search
    candidate_models = [
        "gemini-2.5-flash",           # Tiền đạo mục tiêu (Ưu tiên số 1)
        "gemini-2.0-flash-lite",      # Dự phòng tốc độ
        "gemini-flash-lite-latest",   # Dự phòng ổn định
        "gemini-2.0-flash",           # Bản Flash 2.0 tiêu chuẩn
        "gemini-flash-latest"         # Chốt chặn cuối cùng
    ]
    
    last_error = None
    for model_name in candidate_models:
        for attempt in range(2):
            try:
                # Cấu hình chuẩn xác cho dòng Gemini
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=[{"google_search": {}}],
                    temperature=0.7,
                    max_output_tokens=2048
                )
                response = client.models.generate_content(
                    model=model_name,
                    contents=history,
                    config=config
                )
                return response, model_name
            except Exception as e:
                last_error = e
                error_str = str(e)
                
                # Nếu hết hạn mức (429) hoặc lỗi vùng (400)
                if "429" in error_str or "400" in error_str:
                    print(f"⚠️ {model_name} phản hồi lỗi, đang đổi model...")
                    # Nghỉ lâu hơn một chút (2.5s) để Google reset trạng thái IP/Key
                    time.sleep(2.5) 
                    continue
                else:
                    # Các lỗi nghiêm trọng khác thì bỏ qua model này luôn
                    break
    raise last_error

# 7. Quản lý lịch sử Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. Xử lý câu hỏi người dùng
if prompt := st.chat_input("Hỏi Guru về phim hoặc game..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Guru đang phân tích dữ liệu..."):
                # ĐỒNG BỘ: Chỉ gửi 6 tin nhắn gần nhất để tiết kiệm Token/Quota
                # Giúp tránh lỗi 429 cực kỳ hiệu quả khi nhiều người dùng
                recent_messages = st.session_state.messages[-6:]
                
                formatted_history = []
                for m in recent_messages:
                    role = "user" if m["role"] == "user" else "model"
                    formatted_history.append({"role": role, "parts": [{"text": m["content"]}]})

                response, used_model = call_gemini_smart(formatted_history)
            
            full_response = response.text
            st.markdown(full_response)
            
            # Caption thông tin bổ trợ
            st.caption(f"🚀 Trình diễn bởi {used_model} | 📅 Today: {date_str}")
            if response.candidates[0].grounding_metadata and response.candidates[0].grounding_metadata.search_entry_point:
                st.caption("🌐 Đã kiểm chứng qua Google Search thực tế")

        except Exception as e:
            st.error("⚠️ Guru đang bị nhiễu sóng (Quá tải hạn mức).")
            st.warning("Vui lòng đợi khoảng 30-60 giây để hệ thống hồi phục công lực rồi nhấn gửi lại nhé!")
            with st.expander("Dành cho kỹ thuật viên (Lỗi 429/400)"):
                st.code(str(e))
            full_response = "Lỗi kết nối API hoặc hết hạn mức sử dụng gói Free."

    st.session_state.messages.append({"role": "assistant", "content": full_response})