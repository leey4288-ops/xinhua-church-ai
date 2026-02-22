from openai import OpenAI
import time
import streamlit as st
st.write(st.secrets["OPENAI_API_KEY"][:10])  # 只顯示前 10 個字
# ==============================
# 頁面設定
# ==============================
st.set_page_config(
    page_title="新化教會 AI 同工",
    page_icon="⛪"
)

# ==============================
# 初始化 OpenAI 客戶端
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

# =====================================
# 教會知識庫
# =====================================
KNOWLEDGE = {

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


# ==============================
# 側邊欄
# ==============================
role = st.sidebar.radio("選擇模式", list(ROLES.keys()))
st.title("⛪ 新化教會 AI 同工")

# 防止狂按
if "last_time" not in st.session_state:
    st.session_state.last_time = 0

# ==============================
# 使用者輸入
# ==============================
user_input = st.chat_input("請輸入您的問題")

if user_input:
    # 防止短時間重複按
    if time.time() - st.session_state.last_time < 1:
        st.warning("請稍候")
        st.stop()
    st.session_state.last_time = time.time()

    st.chat_message("user").write(user_input)

    # 組合系統提示
    system_prompt = f"""
{ROLES[role]}

背景資訊：
{KNOWLEDGE[role]}

請用溫暖、自然、符合教會氛圍的方式回應：
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