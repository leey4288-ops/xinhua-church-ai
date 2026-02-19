import random
import streamlit as st
from google import genai
from streamlit_mic_recorder import mic_recorder

# --- 1. 安全讀取 API KEY ---
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "您的備用Key"

client = genai.Client(api_key=API_KEY)

# --- 2. 初始化 Session State (增強防護) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_grid" not in st.session_state:
    st.session_state.selected_grid = None

# --- 3. 靜態資料庫 (維持現狀) ---
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
    "福音陪談": "你現在是『新化教會-福音陪談者』。語氣溫柔真誠，以陪伴為核心。請用溫和的口吻回答問題。",
    "新朋友導覽": "你現在是『新化教會-數位接待員』。熱情引導新朋友了解教會生活與環境。",
    "門徒裝備": "你現在是『新化教會-門徒裝備助手』。鼓勵信徒扎根真理，深化靈命成長。"
}

# --- 4. 側邊欄設計 ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1438232992991-995b7058bbb3?q=80&w=1000", caption="新化長老教會")
    st.title("⛪ 服事選單")
    role_choice = st.radio("選擇模式：", list(DETAILED_PROMPTS.keys()), key="role_radio")

    st.markdown("---")
    # 這裡加入一個簡單的模式說明，幫助同工理解
    st.info(f"目前正在使用：**{role_choice}** 模式")

    if role_choice == "門徒裝備":
        st.subheader("🛠️ 門徒 12 格圖導覽")
        grids = ["01 生命主權", "02 讀經靈修", "03 禱告生活", "04 團契生活", "05 聖潔生活", "06 見證分享",
                 "07 事奉人生", "08 奉獻生活", "09 屬靈爭戰", "10 大使命", "11 肢體連結", "12 永恆盼望"]
        cols = st.columns(2)
        for i, title in enumerate(grids):
            if cols[i % 2].button(title, key=f"btn_12_{i}", use_container_width=True):
                st.session_state.selected_grid = {"type": "門徒", "title": title}
                st.session_state.messages.append({"role": "assistant", "content": f"好的，我們來聊聊 **{title}**。"})
                st.rerun()
    elif role_choice == "福音陪談":
        st.subheader("🎨 福音 10 格圖導覽")
        grids = ["01 創造", "02 墮落", "03 審判", "04 律法", "05 基督", "06 救贖", "07 復活", "08 信心", "09 重生", "10 永生"]
        cols = st.columns(2)
        for i, title in enumerate(grids):
            if cols[i % 2].button(title, key=f"btn_10_{i}", use_container_width=True):
                st.session_state.selected_grid = {"type": "福音", "title": title}
                st.session_state.messages.append({"role": "assistant", "content": f"好的，關於福音十格圖中的 **{title}**..."})
                st.rerun()

    st.markdown("---")
    if st.sidebar.button("🔄 清除對話紀錄", use_container_width=True):
        st.session_state.messages = []
        st.session_state.selected_grid = None
        st.rerun()

# --- 5. 主頁面渲染 ---
# 使用安全獲取方式
selected_grid = st.session_state.get("selected_grid")

if len(st.session_state.messages) <= 1 or selected_grid:
    daily_verse = random.choice(BIBLE_VERSES)
    UI_THEME = {
        "福音陪談": {"color": "#E8F5E9", "border": "#4CAF50", "icon": "🌱", "title": "心靈午茶 - 福音陪談"},
        "新朋友導覽": {"color": "#E3F2FD", "border": "#2196F3", "icon": "👋", "title": "首訪歡迎 - 數位接待"},
        "門徒裝備": {"color": "#FFF3E0", "border": "#FF9800", "icon": "📖", "title": "生命進深 - 門徒裝備"}
    }
    theme = UI_THEME[role_choice]

    display_title = theme['title']
    display_content = "可以直接點選左側教材，或在下方用「說」的跟我聊天喔！"

    if selected_grid:
        display_title = f"{selected_grid['title']}"
        display_content = f"正在與您一同探討 **{selected_grid['title']}** 的真理。"

    st.markdown(f"""
    <div style="background-color: {theme['color']}; padding: 25px; border-radius: 15px; border-left: 8px solid {theme['border']}; margin-bottom: 20px;">
        <h2 style="color: {theme['border']}; margin-top: 0;">{theme['icon']} {display_title}</h2>
        <div style="background-color: white; padding: 15px; border-radius: 10px; margin: 15px 0; border: 1px solid #ddd;">
            <p style="color: #555; font-style: italic; font-size: 1.1em; margin-bottom: 5px;">📖 今日金句：</p>
            <p style="color: {theme['border']}; font-weight: bold; font-size: 1.4em;">{daily_verse}</p>
        </div>
        <p style="color: #444; font-size: 1.3em; line-height: 1.6;">{display_content}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. 對話顯示區 ---
# 先顯示歷史紀錄，確保順序正確
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.markdown(f"### {msg['content']}")
        else:
            st.write(msg["content"])

st.markdown("---")

# --- 7. 輸入區 (語音 + 文字) ---
st.write("🎙️ **長輩語音輸入區**：")

# 修正重點：
# 1. 全部參數使用「名稱=值」的寫法 (具名參數)
# 2. 加入 just_once=True 確保錄音行為符合預期
# 3. 確保 key 的生成邏輯在所有模式下都一致
audio_data = mic_recorder(
    start_prompt="👉 點我開始說話",
    stop_prompt="✅ 說完了，傳送",
    just_once=True,
    use_browser_recognition=True,
    key=f"mic_rec_v3_{role_choice}_{len(st.session_state.messages)}"
)

# 獲取輸入
input_text = st.chat_input("或在此輸入文字...", key="main_input")
voice_text = None

# 【關鍵防錯】確保 audio_data 不是 None 且格式正確才讀取
if audio_data and isinstance(audio_data, dict) and 'transcription' in audio_data:
    voice_text = audio_data['transcription']
    if voice_text:
        st.success(f"語音辨識成功：{voice_text}")

final_prompt = input_text or voice_text

if final_prompt:
    # 立即將使用者的輸入加入清單並渲染
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"):
        st.write(final_prompt)

    with st.chat_message("assistant"):
        with st.spinner("同工正在思考中..."):
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    config={
                        "system_instruction": f"{DETAILED_PROMPTS[role_choice]}\n\n{KNOWLEDGE_BASE[role_choice]}"
                    },
                    contents=[final_prompt]
                )

                if response.text:
                    st.markdown(f"### {response.text}")
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    st.rerun() # 重新整理以確保 UI 更新正確
            except Exception as e:
                st.error(f"連線異常，請稍後再試：{str(e)}")

# 開場白初始化
if len(st.session_state.messages) == 0:
    greetings = {
        "福音陪談": "平安！我是新化教會的數位同工，很高興能陪您聊天。今天想聊聊信仰嗎？",
        "新朋友導覽": "歡迎來到新化長老教會！我是數位接待員，有什麼我可以幫您的嗎？",
        "門徒裝備": "弟兄姊妹平安！今天想在哪個真理上紮根學習呢？"
    }
    st.session_state.messages.append({"role": "assistant", "content": greetings[role_choice]})
    st.rerun()