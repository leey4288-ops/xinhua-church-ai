import random
import streamlit as st
from google import genai

# --- 1. 安全讀取 API KEY ---
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "您的備用Key"

# --- 2. 初始化 Client ---
# 移除所有 http_options 讓 SDK 自動處理連線
client = genai.Client(api_key=API_KEY)

# --- 3. 靜態資料庫 (維持現狀) ---
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

# --- 4. 側邊欄 ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1438232992991-995b7058bbb3?q=80&w=1000", caption="新化長老教會")
    st.title("⛪ 服事選單")
    role_choice = st.radio("選擇模式：", list(DETAILED_PROMPTS.keys()), key="role_radio")
    st.markdown("---")
    st.info(f"模式：**{role_choice}**")
    st.warning("⚠️ 系統不會記錄您的詢問紀錄。")

# --- 5. 主畫面 ---
st.markdown(f"### ⛪ 目前模式：{role_choice}")
st.write("請在下方輸入您的問題。")
st.markdown("---")

# --- 6. 對話邏輯 (無狀態、省耗損、不留紀錄) ---
user_input = st.chat_input("請輸入問題...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("同工正在思考..."):
            try:
                # 【終極優化】指令合併法
                # 1. 徹底不使用 system_instruction 參數，避開 400/404 錯誤
                # 2. 將指令直接與問題合併，確保 AI 依然知道自己的身分
                prompt_combined = f"【身分設定】{DETAILED_PROMPTS[role_choice]}\n【參考知識】{KNOWLEDGE_BASE[role_choice]}\n\n【使用者問題】{user_input}"

                # 3. contents 只傳送目前的這句話，不帶歷史，省 API 耗損且不留紀錄
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[prompt_combined],
                    config={
                        "temperature": 0.7,
                        "max_output_tokens": 400,  # 限制長度省 Token
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