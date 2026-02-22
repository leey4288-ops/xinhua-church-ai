import streamlit as st
import requests
import time

# =====================================
# 基本設定
# =====================================
st.set_page_config(
    page_title="新化教會 AI 同工",
    page_icon="⛪"
)

# =====================================
# 讀取 HuggingFace API Key
# =====================================
try:
    HF_API_KEY = st.secrets["HF_API_KEY"]
except:
    st.error("請在 Streamlit Secrets 設定 HF_API_KEY")
    st.stop()

# ⭐ 新版 HuggingFace Router API
MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_NAME}"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# =====================================
# 教會角色設定
# =====================================
ROLES = {
    "福音陪談": "你是溫柔、有愛心的福音陪談者。",
    "門徒裝備": "你是門徒裝備助手。",
    "新朋友導覽": "你是親切的教會接待同工。"
}

KNOWLEDGE = {
    "福音陪談": "福音包含創造、墮落、救贖與永生。",
    "門徒裝備": "門徒需要讀經、禱告、團契與事奉。",
    "新朋友導覽": "主日聚會 09:30 台南市新化區。"
}

# =====================================
# UI
# =====================================
role = st.sidebar.radio("選擇模式", list(ROLES.keys()))
st.title("⛪ 新化教會 AI 同工")

if "last_time" not in st.session_state:
    st.session_state.last_time = 0

user_input = st.chat_input("請輸入您的問題")

if user_input:

    if time.time() - st.session_state.last_time < 1:
        st.warning("請稍候")
        st.stop()

    st.session_state.last_time = time.time()

    st.chat_message("user").write(user_input)

    prompt = f"""
{ROLES[role]}

背景資訊：
{KNOWLEDGE[role]}

請用溫暖自然的方式回答：

{user_input}
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 400,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    try:
        with st.spinner("思考中..."):
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=120
            )

        result = response.json()

        if response.status_code != 200:
            st.error(f"HTTP 錯誤碼: {response.status_code}")
            st.code(response.text)
            st.stop()

        try:
            result = response.json()
        except Exception:
            st.error("回傳不是 JSON 格式")
            st.code(response.text)
            st.stop()

    st.chat_message("assistant").write(reply)

else:
    st.write("🙏 平安，請輸入您的問題")