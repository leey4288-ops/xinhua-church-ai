import random
import streamlit as st
from google import genai  # 確保使用新版 SDK 匯入方式

# --- 1. 安全讀取 API KEY ---
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "您的備用Key"

# 【核心修正】初始化 Client
# 不指定 api_version，讓 SDK 1.64.0 自動選擇最穩定的 v1 路徑
client = genai.Client(api_key=API_KEY)

# --- 2. 靜態資料庫 (減少 Session 記憶體負擔) ---
KNOWLEDGE_BASE = {
    "福音陪談": "【福音 10 格圖】1.創造 2.墮落 3.審判 4.律法 5.基督 6.救贖 7.復活 8.信心 9.重生 10.永生。",
    "門徒裝備": "【門徒 12 格圖】1.生命主權 2.讀經靈修 3.禱告生活 4.團契生活 5.聖潔生活 6.見證分享 7.事奉人生 8.奉獻生活 9.屬靈爭戰 10.大使命 11.肢體連結 12.永恆盼望。",
    "新朋友導覽": "【教會資訊】聚會時間週日上午 09:30。地點在台南市新化區，歡迎新朋友。"
}

DETAILED_PROMPTS = {
    "福音陪談": "你現在是『新化教會-福音陪談者』。語氣溫柔真誠。",
    "新朋友導覽": "你現在是『新化教會-數位接待員』。熱情引導。",
    "門徒裝備": "你現在是『新化教會-門徒裝備助手』。鼓勵扎根。"
}

# --- 3. 側邊欄與 UI ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1438232992991-995b7058bbb3?q=80&w=1000")
    role_choice = st.radio("選擇模式：", list(DETAILED_PROMPTS.keys()), key="role_radio")
    st.info(f"模式：**{role_choice}**")

st.markdown(f"### ⛪ 目前模式：{role_choice}")
st.markdown("---")

# --- 4. 對話邏輯 (無狀態、省耗損、不留紀錄) ---
user_input = st.chat_input("請輸入問題...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("同工正在思考..."):
            try:
                # 【恢復 2/18 穩定性】合併指令法：
                # 避開 system_instruction 參數，從根源解決 404/400 報錯
                prompt_combined = f"指令：{DETAILED_PROMPTS[role_choice]}\n知識庫：{KNOWLEDGE_BASE[role_choice]}\n\n問題：{user_input}"

                # contents 只傳送單次問題，達成「不保留紀錄」且「節省 API 耗損」
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[prompt_combined],
                    config={
                        "temperature": 0.7,
                        "max_output_tokens": 400,  # 限制長度節省耗損
                        "top_p": 0.95
                    }
                )

                if response and response.text:
                    st.markdown(f"### {response.text}")

            except Exception as e:
                st.error("連線目前較為忙碌，請重新輸入一次。")
                with st.expander("除錯資訊"):
                    st.code(str(e))
else:
    st.write("🙏 平安！請問今天有什麼我可以幫您的嗎？")