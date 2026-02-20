import random
import streamlit as st
from google import genai

# --- 1. 安全讀取 API KEY ---
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "您的備用Key"

# 初始化 Client (1.64.0 版建議寫法)
client = genai.Client(api_key=API_KEY)

# --- 2. 靜態資料庫 (減少 Session 記憶體負擔) ---
BIBLE_VERSES = [
    "「應當一無掛慮...」— 腓立比書 4:6",
    "「你的話是我腳前的燈...」— 詩篇 119:105",
    "「耶和華是我的牧者，我必不致缺乏。」— 詩篇 23:1"
]

KNOWLEDGE_BASE = {
    "福音陪談": "【福音 10 格圖】1.創造...10.永生。",
    "門徒裝備": "【門徒 12 格圖】1.生命主權...12.永恆盼望。",
    "新朋友導覽": "【教會資訊】聚會時間週日上午 09:30。"
}

DETAILED_PROMPTS = {
    "福音陪談": "你現在是『新化教會-福音陪談者』。語氣溫柔。",
    "新朋友導覽": "你現在是『新化教會-數位接待員』。熱情引導。",
    "門徒裝備": "你現在是『新化教會-門徒裝備助手』。鼓勵成長。"
}

# --- 3. 側邊欄 ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1438232992991-995b7058bbb3?q=80&w=1000")
    role_choice = st.radio("選擇模式：", list(DETAILED_PROMPTS.keys()), key="role_radio")
    st.info(f"模式：**{role_choice}**")
    st.warning("⚠️ 系統不會記錄您的詢問，關閉後紀錄即消失。")

# --- 4. 主畫面渲染 ---
st.markdown(f"### 📖 今日金句：\n> {random.choice(BIBLE_VERSES)}")
st.markdown("---")

# --- 5. 對話邏輯 (單次問答 + 修正 404) ---

# 使用文字輸入框
user_input = st.chat_input("請輸入您的問題...")

if user_input:
    # 顯示使用者當前問題
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("同工正在思考中..."):
            try:
                # 合併指令與問題，這是不報錯、不留歷史紀錄的最佳做法
                full_prompt = f"指令：{DETAILED_PROMPTS[role_choice]}\n知識庫：{KNOWLEDGE_BASE[role_choice]}\n\n問題：{user_input}"

                # 【關鍵修正】使用完整的模型路徑 models/gemini-1.5-flash
                # 這能解決 API v1 找不到模型的 404 問題
                response = client.models.generate_content(
                    model="models/gemini-1.5-flash",
                    contents=[full_prompt],
                    config={
                        "temperature": 0.7,
                        "max_output_tokens": 400,  # 節省 API 耗損：限制字數
                        "top_p": 0.95
                    }
                )

                if response and response.text:
                    st.markdown(f"### {response.text}")

            except Exception as e:
                st.error("連線異常，請稍後再試。")
                with st.expander("詳細報錯 (除錯用)"):
                    st.code(str(e))
else:
    st.write("🙏 平安！我是教會數位同工，請問有什麼我可以幫您的嗎？")