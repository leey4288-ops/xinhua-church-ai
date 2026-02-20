import time
import streamlit as st
from google import genai

# =============================
# 1️⃣ 安全讀取 API KEY
# =============================
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("請先在 Streamlit Secrets 設定 GEMINI_API_KEY")
    st.stop()

client = genai.Client(api_key=API_KEY)

# =============================
# 2️⃣ 靜態資料庫
# =============================
KNOWLEDGE_BASE = {
    "福音陪談": "【福音 10 格圖】1.創造 2.墮落 3.審判 4.律法 5.基督 6.救贖 7.復活 8.信心 9.重生 10.永生。",
    "門徒裝備": "【門徒 12 格圖】1.生命主權 2.讀經靈修 3.禱告生活 4.團契生活 5.聖潔生活 6.見證分享 7.事奉人生 8.奉獻生活 9.屬靈爭戰 10.大使命 11.肢體連結 12.永恆盼望。",
    "新朋友導覽": "【教會資訊】聚會時間週日上午 09:30。地點在台南市新化區，歡迎新朋友。"
}

DETAILED_PROMPTS = {
    "福音陪談": "你現在是『新化教會-福音陪談者』。語氣溫柔真誠，請用溫和的口吻回答問題。",
    "新朋友導覽": "你現在是『新化教會-數位接待員』。熱情引導新朋友了解教會。",
    "門徒裝備": "你現在是『新化教會-門徒裝備助手』。鼓勵信徒扎根真理。"
}

# =============================
# 3️⃣ 側邊欄
# =============================
with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1438232992991-995b7058bbb3?q=80&w=1000",
        caption="新化長老教會"
    )
    st.title("⛪ 服事選單")

    role_choice = st.radio("選擇模式：", list(DETAILED_PROMPTS.keys()))

    st.markdown("---")
    st.info(f"模式：**{role_choice}**")
    st.warning("⚠️ 系統不會記錄您的詢問，保護隱私。")

# =============================
# 4️⃣ 主畫面
# =============================
st.markdown(f"### ⛪ 目前模式：{role_choice}")
st.write("請在下方輸入您的問題，數位同工將竭誠為您服務。")
st.markdown("---")

# =============================
# 5️⃣ 防止連續狂按
# =============================
if "last_call" not in st.session_state:
    st.session_state.last_call = 0

# =============================
# 6️⃣ 單次問答
# =============================
user_input = st.chat_input("請在此輸入您的問題...")

if user_input:

    if time.time() - st.session_state.last_call < 2:
        st.warning("請稍候再詢問 🙏")
        st.stop()

    st.session_state.last_call = time.time()

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("同工正在思考中..."):

            try:
                prompt_combined = f"""
角色指令：
{DETAILED_PROMPTS[role_choice]}

背景知識：
{KNOWLEDGE_BASE[role_choice]}

使用者問題：
{user_input}

請用溫柔、自然、符合角色的方式回答。
"""

                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt_combined,
                    config={
                        "temperature": 0.7,
                        "max_output_tokens": 400,
                        "top_p": 0.9,
                    }
                )

                reply = getattr(response, "text", None)

                if reply:
                    st.markdown(reply)
                else:
                    st.warning("暫時無法取得回應，請再試一次。")

            except Exception as e:
                st.error("連線目前較為忙碌，請重新輸入一次。")
                with st.expander("除錯資訊 (開發者參考)"):
                    st.code(str(e))

else:
    st.write("🙏 平安！請問今天有什麼我可以幫您的嗎？")