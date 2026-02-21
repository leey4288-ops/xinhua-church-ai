import streamlit as st
import requests
import time

st.set_page_config(
    page_title="新化教會 AI 同工",
    page_icon="⛪"
)

# API KEY
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    st.error("請設定 OPENROUTER_API_KEY")
    st.stop()

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

role = st.sidebar.radio(
    "選擇模式",
    list(ROLES.keys())
)

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
角色：
{ROLES[role]}

背景：
{KNOWLEDGE[role]}

問題：
{user_input}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.7
    }

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        result = response.json()

        reply = result["choices"][0]["message"]["content"]

    except Exception as e:

        reply = str(e)

    st.chat_message("assistant").write(reply)

else:

    st.write("🙏 平安，請輸入您的問題")