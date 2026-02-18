import random
import streamlit as st
import google.generativeai as genai

# --- 1. 安全讀取 API KEY ---
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "您的備用Key"

genai.configure(api_key=API_KEY)

# --- 2. 初始化 Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_grid" not in st.session_state:
    st.session_state.selected_grid = None

# --- 3. 靜態資料庫 ---
BIBLE_VERSES = [
    "「應當一無掛慮，只要凡事藉著禱告、祈求，和感謝，將你們所要的告訴神。」— 腓立比書 4:6",
    "「你的話是我腳前的燈，是我路上的光。」— 詩篇 119:105",
    "「我們曉得萬事都互相效力，叫愛神的人得益處。」— 羅馬書 8:28",
    "「耶和華是我的牧者，我必不致缺乏。」— 詩篇 23:1",
    "「神愛世人，甚至將他的獨生子賜給他們，叫一切信他的，不至滅亡，反得永生。」— 約翰福音 3:16"
]

DETAILED_PROMPTS = {
    "福音陪談": "你現在是『新化教會-福音陪談者』。語氣溫柔真誠，以陪伴為核心。主要使用福音10格圖引導慕道友。",
    "新朋友導覽": "你現在是『新化教會-數位接待員』。熱情引導新朋友了解教會生活、聚會時間(09:20)與環境。",
    "門徒裝備": "你現在是『新化教會-門徒裝備助手』。鼓勵信徒扎根真理，使用12格圖進行靈命成長訓練。"
}

CHURCH_KNOWLEDGE = """
【核心教材一：福音 10 格圖（慕道/陪談用）】
1.創造 2.墮落 3.審判 4.律法 5.基督 6.救贖 7.復活 8.信心 9.重生 10.永生。
【核心教材二：門徒 12 格圖（信徒/裝備用）】
1.生命主權 2.讀經靈修 3.禱告生活 4.團契生活 5.聖潔生活 6.見證分享 
7.事奉人生 8.奉獻生活 9.屬靈爭戰 10.大使命 11.肢體連結 12.永恆盼望。
【引導指令】回覆末端請標註進度，例如：(進度：福音第5格-基督)。
"""

# --- 4. 側邊欄設計 ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1438232992991-995b7058bbb3?q=80&w=1000", caption="新化長老教會")
    st.title("⛪ 服事選單")
    role_choice = st.radio("選擇模式：", list(DETAILED_PROMPTS.keys()))

    st.markdown("---")
    if role_choice == "門徒裝備":
        st.subheader("🛠️ 門徒 12 格圖導覽")
        grids_12 = ["01 生命主權", "02 讀經靈修", "03 禱告生活", "04 團契生活", "05 聖潔生活", "06 見證分享",
                    "07 事奉人生", "08 奉獻生活", "09 屬靈爭戰", "10 大使命", "11 肢體連結", "12 永恆盼望"]
        cols = st.columns(2)
        for i, title in enumerate(grids_12):
            if cols[i % 2].button(title, key=f"btn_{role_choice}_{i}", use_container_width=True):
                st.session_state.selected_grid = {"type": "門徒", "title": title}
                st.session_state.messages.append({"role": "assistant", "content": f"已切換至：**門徒裝備 - {title}**"})
                st.rerun()
    elif role_choice == "福音陪談":
        st.subheader("🎨 福音 10 格圖導覽")
        grids_10 = ["01 創造", "02 墮落", "03 審判", "04 律法", "05 基督", "06 救贖", "07 復活", "08 信心", "09 重生", "10 永生"]
        cols = st.columns(2)
        for i, title in enumerate(grids_10):
            if cols[i % 2].button(title, key=f"btn_{role_choice}_{i}", use_container_width=True):
                st.session_state.selected_grid = {"type": "福音", "title": title}
                st.session_state.messages.append({"role": "assistant", "content": f"已切換至：**福音十格圖 - {title}**"})
                st.rerun()

    st.markdown("---")
    if st.sidebar.button("🔄 清除對話紀錄"):
        st.session_state.messages = []
        st.session_state.selected_grid = None
        st.rerun()

# --- 5. 主頁面動態渲染 ---
if len(st.session_state.messages) <= 1 or st.session_state.selected_grid:
    daily_verse = random.choice(BIBLE_VERSES)
    UI_THEME = {
        "福音陪談": {"color": "#E8F5E9", "border": "#4CAF50", "icon": "🌱", "title": "心靈午茶 - 福音陪談"},
        "新朋友導覽": {"color": "#E3F2FD", "border": "#2196F3", "icon": "👋", "title": "首訪歡迎 - 數位接待"},
        "門徒裝備": {"color": "#FFF3E0", "border": "#FF9800", "icon": "📖", "title": "生命進深 - 門徒裝備"}
    }
    theme = UI_THEME[role_choice]

    if st.session_state.selected_grid:
        grid = st.session_state.selected_grid
        display_title = f"{grid['type']}裝備：{grid['title']}"
        display_content = f"正在深入學習 **{grid['title']}** 的核心真理。您可以詢問相關經文或實踐方法。"
        if st.button("⬅️ 回到首頁"):
            st.session_state.selected_grid = None
            st.rerun()
    else:
        display_title = theme['title']
        display_content = "我們致力於成為一個充滿愛與真理的大家庭。請選擇左側教材開始學習，或直接在下方輸入問題。"

    st.markdown(f"""
    <div style="background-color: {theme['color']}; padding: 25px; border-radius: 15px; border-left: 8px solid {theme['border']}; margin-bottom: 20px;">
        <h2 style="color: {theme['border']}; margin-top: 0;">{theme['icon']} {display_title}</h2>
        <div style="background-color: white; padding: 15px; border-radius: 10px; margin: 15px 0; border: 1px solid #ddd;">
            <p style="color: #555; font-style: italic; margin-bottom: 5px;">📖 今天的亮光：</p>
            <p style="color: {theme['border']}; font-weight: bold; font-size: 1.1em;">{daily_verse}</p>
        </div>
        <p style="color: #444; font-size: 1.1em;">{display_content}</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.selected_grid:
        st.subheader(f"💡 您可以這樣問 {role_choice}")
        suggestions = {
            "福音陪談": ["我想了解福音 10 格圖", "覺得壓力很大，想請你為我禱告", "耶穌是誰？"],
            "新朋友導覽": ["教會主日在哪裡停車？", "第一次來教會要做什麼？", "附近的推薦美食"],
            "門徒裝備": ["門徒 12 格圖的重點是什麼？", "如何建立穩定的讀經習慣？", "什麼是生命主權？"]
        }
        cols = st.columns(3)
        for idx, text in enumerate(suggestions[role_choice]):
            if cols[idx].button(text, key=f"sug_{idx}"):
                st.info(f"建議提問：{text}")

st.markdown("---")

# --- 6. 對話邏輯 ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if prompt := st.chat_input("請輸入您的問題...", key=f"chat_input_{role_choice}"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(
                model_name="gemini-flash-latest",
                system_instruction=str(f"{DETAILED_PROMPTS[role_choice]}\n\n{CHURCH_KNOWLEDGE}").strip()
            )
            history_data = []
            for m in st.session_state.messages[:-1]:
                if m["content"].strip():
                    role = "user" if m["role"] == "user" else "model"
                    history_data.append({"role": role, "parts": [str(m["content"])]})

            chat = model.start_chat(history=history_data)
            response = chat.send_message(str(prompt), request_options={"timeout": 60.0})

            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("⚠️ AI 回傳了空內容。")

        except Exception as e:
            if "503" in str(e):
                st.error("⛪ 教會伺服器（Google API）繁忙中，請點擊『清除對話紀錄』再試。")
            else:
                st.error(f"連線狀態：{e}")

if len(st.session_state.messages) == 0:
    greetings = {"福音陪談": "平安！我是新化教會的數位同工，想聊聊信仰嗎？",
                 "新朋友導覽": "歡迎！想了解教會環境還是聚會時間呢？",
                 "門徒裝備": "弟兄姊妹平安！今天想學習哪一部分的教材？"}
    st.session_state.messages.append({"role": "assistant", "content": greetings[role_choice]})
    st.rerun()