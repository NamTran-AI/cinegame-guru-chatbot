import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

# Cấu hình trang Web
st.set_page_config(page_title="CineGame Guru", page_icon="🎮")
st.title("🎮 CineGame Guru AI")
st.caption("Chuyên gia giải trí - RAG & Search Powered")

# Khởi tạo Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Load tri thức
@st.cache_data
def get_knowledge():
    if os.path.exists("knowledge.txt"):
        with open("knowledge.txt", "r", encoding="utf-8") as f:
            return f.read()
    return ""

knowledge = get_knowledge()

# Khởi tạo tin nhắn trong phiên làm việc
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Người dùng nhập câu hỏi
if prompt := st.chat_input("Hỏi Guru về game hoặc phim..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gọi AI trả lời
    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=f"Bạn là CineGame Guru. Tri thức nội bộ: {knowledge}",
                tools=[{"google_search": {}}]
            )
        )
        full_response = response.text
        st.markdown(full_response)
        
        if response.candidates[0].grounding_metadata:
            st.info("🌐 Đã xác thực qua Google Search")

    st.session_state.messages.append({"role": "assistant", "content": full_response})