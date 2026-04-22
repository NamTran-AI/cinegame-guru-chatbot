import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# 1. Tải các biến môi trường
load_dotenv()

# 2. Cấu hình trang Web
st.set_page_config(
    page_title="CineGame Guru | AI Agent", 
    page_icon="🎮", 
    layout="centered"
)

# Tùy chỉnh giao diện một chút cho chuyên nghiệp
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎮 CineGame Guru AI")
st.caption("Advanced RAG System with Real-time Search Grounding")

# 3. Khởi tạo kết nối với Gemini 2.5 Flash
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

# 5. Cấu hình "não bộ" cho Guru
system_instruction = (
    "Bạn là CineGame Guru - Một thực thể AI siêu cấp am hiểu về Điện ảnh và Video Games. "
    "QUY TẮC PHẢN HỒI:\n"
    "1. TẬP TRUNG: Chỉ trả lời duy nhất về chủ đề người dùng đang hỏi. Nếu hỏi về một bộ phim cụ thể (như Iron Man), "
    "tuyệt đối không liệt kê các thông tin về game hay phim khác có trong kho tri thức.\n"
    "2. CHI TIẾT: Câu trả lời phải sâu sắc. Với phim ảnh, phải nêu rõ: Đạo diễn, Dàn diễn viên chính, "
    "Cốt truyện tóm tắt, Doanh thu và các bí ẩn hậu trường (Easter Eggs).\n"
    "3. NGUỒN LỰC: Ưu tiên dữ liệu từ 'knowledge.txt'. Tuy nhiên, nếu dữ liệu đó không đủ chi tiết hoặc quá cũ, "
    "hãy sử dụng Google Search để lấy thông tin chính xác nhất cho năm 2026.\n"
    "4. PHONG CÁCH: Trò chuyện như một chuyên gia, sử dụng định dạng Markdown (Bold, Bullet points) để dễ nhìn.\n\n"
    f"KHO TRI THỨC NỘI BỘ: {knowledge_content}"
)

# 6. Quản lý lịch sử Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Xử lý câu hỏi người dùng
if prompt := st.chat_input("Hỏi Guru về phim hoặc game bạn quan tâm..."):
    # Hiển thị tin nhắn User
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Xử lý phản hồi từ Assistant
    with st.chat_message("assistant"):
        full_response = ""
        try:
            # Gọi mô hình Gemini 2.5 Flash
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=[{"google_search": {}}],
                    temperature=0.7,      # Tăng độ sáng tạo và độ dài
                    max_output_tokens=2500 # Cho phép trả lời rất dài
                )
            )
            
            full_response = response.text
            st.markdown(full_response)
            
            # Hiển thị nguồn Search nếu có
            if response.candidates[0].grounding_metadata:
                st.caption("🌐 Fact-checked via Google Search")

        except Exception as e:
            full_response = "⚠️ Guru đang bị nhiễu sóng hoặc quá tải hạn mức API."
            st.error("Úp sọt! Có lỗi xảy ra hoặc bạn đã dùng hết quota phút này.")
            st.info(f"Lỗi: {e}")

    # Lưu vào lịch sử
    st.session_state.messages.append({"role": "assistant", "content": full_response})