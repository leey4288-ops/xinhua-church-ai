import time
import streamlit as st
from google import genai

# =====================================
# 安全讀取 API KEY
# =====================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("請在 Streamlit Cloud → Settings → Secrets 設定 GEMINI_API_KEY")
    st.stop()

client = genai.Client(api_key=API_KEY)

# =====================================
# 頁面設定
# =====================================
st.set_page_config(
    page_title="新化教會 AI 同工",
    page_icon="⛪",
    layout="centered"
)

# =====================================
# 知識庫
# =====================================
KNOWLEDGE_BASE = {
    "福音陪談":
        "【福音 10 格圖】1創造 2墮落 3審判 4律法 5基督 6救贖 7復活 8信心 9重生 10永生",

    "門徒裝備":
        "【門徒 12 格圖】1生命主權 2讀經 3禱告 4團契 5聖潔 6見證 7事奉 8奉獻 9爭戰 10大使命 11連結 12盼望",

    "新朋友導覽":
        "【教會資訊】主日 09:30 台南市新化區，歡迎新朋友"
}

ROLES = {
    "福音陪談": "你是溫柔的福音陪談者",
    "門徒裝備": "你是門徒裝備助手",
    "新朋友導覽": "你是熱情的教會接待員"
}

# =====================================
# 側邊欄
# =====================================
with st.sidebar:

    st.title("⛪ 新化教會 AI")

    role = st.radio(
        "選擇模式",
        ["福音陪談", "門徒裝備", "新朋友導覽"]
    )

    st.info(f"目前模式：{role}")

# =====================================
# 主畫面
# =====================================
st.title("⛪ 新化教會 AI 同工")

st.write("歡迎，請輸入您的問題")

# 防止狂按
if "last_time" not in st.session_state:
    st.session_state.last_time = 0

# =====================================
# 使用者輸入
# =====================================
prompt = st.chat_input("請輸入...")

if prompt:

    if time.time() - st.session_state.last_time < 2:
        st.warning("請稍候再詢問")
        st.stop()

    st.session_state.last_time = time.time()

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):

        with st.spinner("思考中..."):

            try:

                full_prompt = f"""
角色：
{ROLES[role]}

背景：
{KNOWLEDGE_BASE[role]}

問題：
{prompt}

請用溫柔自然方式回答
"""

                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=full_prompt
                )

                reply = getattr(response, "text", None)

                if reply:
                    st.write(reply)
                else:
                    st.write("請再試一次")

            except Exception as e:

                st.error("系統忙碌中")

                with st.expander("錯誤"):
                    st.code(str(e))

else:

    st.write("🙏 平安，請輸入問題")