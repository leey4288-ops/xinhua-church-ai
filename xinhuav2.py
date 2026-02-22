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

# 使用免費聊天模型（穩定）
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
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
# Sidebar
# =====================================
role = st.sidebar.radio(
    "選擇模式",
    list(ROLES.keys())
)

st.title("⛪ 新化教會 AI 同工")

# =====================================
# 防止狂按
# =====================================
if "last_time" not in st.session_state:
    st.session_state.last_time = 0

# =====================================
# 使用者輸入
# =====================================
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

請用溫暖、自然的方式回答以下問題：

{user_input}
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
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
                timeout=90
            )

        result = response.json()

        # 處理常見錯誤格式
        if isinstance(result, dict) and "error" in result:
            reply = f"API 錯誤：{result['error']}"
        else:
            reply = result[0]["generated_text"]

    except Exception as e:
        reply = f"系統錯誤：{str(e)}"

    st.chat_message("assistant").write(reply)

else:

    st.write("🙏 平安，請輸入您的問題")