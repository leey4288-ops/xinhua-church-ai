import streamlit as st
from openai import OpenAI
import time

# ==============================
# 基本設定
# ==============================
st.set_page_config(
    page_title="新化教會 AI 同工",
    page_icon="⛪"
)

# ==============================
# 讀取 API KEY
# ==============================
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("請在 Streamlit Secrets 設定 OPENAI_API_KEY")
    st.stop()

# ==============================
# 教會角色設定
# ==============================
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

    system_prompt = f"""
{ROLES[role]}

背景資訊：
{KNOWLEDGE[role]}

請用溫暖、自然、符合教會氛圍的方式回應。
"""

    try:

        with st.spinner("思考中..."):

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=600
            )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"系統錯誤：{str(e)}"

    st.chat_message("assistant").write(reply)

else:
    st.write("🙏 平安，請輸入您的問題")