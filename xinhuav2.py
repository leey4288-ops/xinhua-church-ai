import time
import streamlit as st
from google import genai

# =====================================
# 頁面基本設定（必須放最前面）
# =====================================
st.set_page_config(
    page_title="新化教會 AI 同工",
    page_icon="⛪",
    layout="centered"
)

# =====================================
# 安全讀取 API KEY
# =====================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("請在 Streamlit Cloud → Settings → Secrets 設定 GEMINI_API_KEY")
    st.stop()

# 初始化 Gemini Client
client = genai.Client(api_key=API_KEY)

# =====================================
# 教會知識庫
# =====================================
KNOWLEDGE_BASE = {

    "福音陪談":
    """福音 10 格圖：
    1 創造
    2 墮落
    3 審判
    4 律法
    5 基督
    6 救贖
    7 復活
    8 信心
    9 重生
    10 永生""",

    "門徒裝備":
    """門徒 12 格圖：
    1 生命主權
    2 讀經靈修
    3 禱告生活
    4 團契生活
    5 聖潔生活
    6 見證分享
    7 事奉人生
    8 奉獻生活
    9 屬靈爭戰
    10 大使命
    11 肢體連結
    12 永恆盼望""",

    "新朋友導覽":
    """教會資訊：
    主日聚會：週日上午 09:20
    地點：(712003) 台南市新化區中山路207號 電話：06-5902517;06-5903940. 傳真：06-5903502
    歡迎新朋友參加"""
}

# =====================================
# 角色設定
# =====================================
ROLES = {

    "福音陪談":
    "你是新化教會溫柔、有愛心的福音陪談者，請用溫柔與關懷的語氣回答。",

    "門徒裝備":
    "你是新化教會門徒裝備助手，請用鼓勵與造就的語氣回答。",

    "新朋友導覽":
    "你是新化教會親切的接待同工，請熱情歡迎並清楚說明。"
}

# =====================================
# Sidebar
# =====================================
with st.sidebar:

    st.title("⛪ 新化教會 AI 同工")

    role = st.radio(
        "請選擇服事模式",
        ["福音陪談", "門徒裝備", "新朋友導覽"]
    )

    st.markdown("---")

    st.info(f"目前模式：{role}")

    st.caption("系統不會保存對話紀錄")

# =====================================
# 主畫面
# =====================================
st.title("⛪ 新化教會 AI 同工")

st.write("歡迎您，請輸入您的問題 🙏")

st.markdown("---")

# =====================================
# 防止使用者狂按（避免費用暴增）
# =====================================
if "last_call_time" not in st.session_state:
    st.session_state.last_call_time = 0

# =====================================
# 聊天輸入
# =====================================
user_input = st.chat_input("請輸入您的問題...")

if user_input:

    # 限制頻率
    if time.time() - st.session_state.last_call_time < 2:
        st.warning("請稍候再詢問 🙏")
        st.stop()

    st.session_state.last_call_time = time.time()

    # 顯示使用者訊息
    with st.chat_message("user"):
        st.write(user_input)

    # AI 回覆區塊
    with st.chat_message("assistant"):

        with st.spinner("同工正在思考中..."):

            try:

                # 組合 Prompt（最穩定方式）
                full_prompt = f"""
角色設定：
{ROLES[role]}

背景知識：
{KNOWLEDGE_BASE[role]}

使用者問題：
{user_input}

請用溫柔、自然、符合角色的方式回答。
"""

                # ⭐ 使用最新模型 gemini-2.0-flash
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=full_prompt
                )

                # 安全取得回應
                reply = getattr(response, "text", None)

                if reply:
                    st.write(reply)
                else:
                    st.warning("目前無法取得回應，請再試一次。")

            except Exception as e:

                st.error("系統忙碌中，請稍後再試")

                with st.expander("錯誤詳情"):
                    st.code(str(e))

else:

    st.write("🙏 平安！歡迎詢問任何問題")