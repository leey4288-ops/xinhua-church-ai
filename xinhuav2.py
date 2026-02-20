import random
import streamlit as st
from google import genai

# --- 1. 安全讀取 API KEY ---
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "您的備用Key"

# --- 1. 初始化 Client (強制指定穩定版 API v1) ---
client = genai.Client(
    api_key=API_KEY,
    http_options={'api_version': 'v1'}
)

# --- 2. 靜態資料庫 (減少 Session 負擔) ---
BIBLE_VERSES = [
    "「應當一無掛慮，只要凡事藉著禱告、祈求，和感謝，將你們所要的告訴神。」— 腓立比書 4:6",
    "「你的話是我腳前的燈，是我路上的光。」— 詩篇 119:105",
    "「我們曉得萬事都互相效力，叫愛神的人得益處。」— 羅馬書 8:28",
    "「耶和華是我的牧者，我必不致缺乏。」— 詩篇 23:1",
    "「神愛世人，甚至將他的獨生子賜給他們，叫一切信他的，不至滅亡，反得永生。」— 約翰福音 3:16"
]

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

# --- 3. 側邊欄設計 ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1438232992991-995b7058bbb3?q=80&w=1000", caption="新化長老教會")
    st.title("⛪ 服事選單")
    role_choice = st.radio("選擇模式：", list(DETAILED_PROMPTS.keys()), key="role_radio")

    st.markdown("---")
    st.info(f"目前模式：**{role_choice}**")
    st.warning("⚠️ 為了保護隱私，本系統不會記錄您的對話，關閉網頁後紀錄即消失。")

# --- 4. 主頁面渲染 ---
daily_verse = random.choice(BIBLE_VERSES)
UI_THEME = {
    "福音陪談": {"color": "#E8F5E9", "border": "#4CAF50", "icon": "🌱", "title": "心靈午茶 - 福音陪談"},
    "新朋友導覽": {"color": "#E3F2FD", "border": "#2196F3", "icon": "👋", "title": "首訪歡迎 - 數位接待"},
    "門徒裝備": {"color": "#FFF3E0", "border": "#FF9800", "icon": "📖", "title": "生命進深 - 門徒裝備"}
}
theme = UI_THEME[role_choice]

st.markdown(f"""
<div style="background-color: {theme['color']}; padding: 25px; border-radius: 15px; border-left: 8px solid {theme['border']};">
    <h2 style="color: {theme['border']}; margin-top: 0;">{theme['icon']} {theme['title']}</h2>
    <div style="background-color: white; padding: 15px; border-radius: 10px; margin: 15px 0; border: 1px solid #ddd;">
        <p style="color: {theme['border']}; font-weight: bold; font-size: 1.4em;">{daily_verse}</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- 5. 對話邏輯 (優化：單次問答，不佔用 Session 記憶) ---

user_input = st.chat_input("請在此輸入您的問題...")

if user_input:
    with st.chat_message("assistant"):
        with st.spinner("同工正在思考中..."):
            try:
                # 1. 準備系統指令與知識庫
                instruction = f"{DETAILED_PROMPTS[role_choice]}\n背景知識：{KNOWLEDGE_BASE[role_choice]}"

                # 2. 【核心優化】採用「指令+問題」合併法 (最穩定，不報錯)
                # 這種寫法不使用 system_instruction 參數，完全避開 Pydantic 驗證錯誤
                # contents 僅包含當前問題，不帶歷史紀錄，達成「不保留紀錄」且「節省 API 耗損」
                prompt_with_context = f"指令：{instruction}\n\n使用者問題：{user_input}"

                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[prompt_with_context],
                    config={
                        "temperature": 0.7,
                        "max_output_tokens": 400,  # 限制長度節省耗損
                        "top_p": 0.95
                    }
                )

                if response and response.text:
                    st.markdown(f"### {response.text}")

            except Exception as e:
                st.error("目前連線忙碌，請稍後再試。")
                with st.expander("詳細錯誤 (Debug 用)"):
                    st.code(str(e))