from openai import OpenAI
import time
import streamlit as st

st.write(st.secrets["OPENAI_API_KEY"][:10])  # 只顯示前 10 個字

# ==============================
# 頁面設定
# ==============================
st.set_page_config(
    page_title="新化教會 AI 同工",
    page_icon="logo.png"

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
    """設立日期：
    1915/1/1

    牧者姓名：
    陳毅哲牧師﹙傳道師代號：81912﹚
    吳純芳牧師﹙傳道師代號：81913﹚

    禮拜時間：
    台語 - 禮拜日 上午 09:20
    華語 - 禮拜日 上午 10:50

    地點：
    (712003) 台南市新化區中山路207號 
    電話：06-5902517;06-5903940. 
    傳真：06-5903502
    電子信箱：sinhoachurch@gmail.com
    
    資源設施：
    【松年大學】台灣基督長老教會松年大學新化分校
    【教育設施】台南市新化博愛關懷協會

    各項聚會：
    禱告會
    青少年團契
    兒童主日學
    聖歌隊

    新化教會簡史
    百年前就有基督徒在大目降附居住，主後1915年1月1日，李照耀長老等數名信徒謨議，由新和教會劉俊臣牧師主領，成立新化教會。起初新化信徒在王公廳後方租一間閒置的土确厝牛廄聚會，2
    年後原租處破爛不堪使用，遷往李照耀長老住處聚會。因缺乏傳教者前來駐會，乃洽請台南神學院派遣神學生前來協助聖工之推展，後因信徒增加，李照耀捐出土地600坪建堂，1922
    年5月第一代紅磚瓦禮拜堂落成。自此教勢日隆信徒益眾。

1953
年9月4日分設口埤教會，
1956
年又創辦「育英幼稚園」並獲台南縣政府准予立案，
1971
年5月23日舉行現在的新堂之奠基禮拜，同年11月12日舉行新會堂獻堂禮拜，
1976
年7月重建牧師館一座，於同年12月31日舉行牧師館落成感恩禮拜，
1999
年6月1日正式完成教育館它建立於禮拜堂之後方。

2015
年慶祝設教百週年，舉辦百週年慶系列活動。
2015
年1月18日舉行設教百週年感恩禮拜；8
月9日主日禮拜舉行「百週年慶家庭節」，邀請教會家庭會友家庭介紹各家庭特色。新化教會歷經百年發展，社區事工也從過去的幼兒教育，拓展到今日開辦松年大學、品格學校、英語查經班，教會各團契與小組牧養關懷，持續關心地方弱勢、青少年及長者。

歡迎新朋友參加""",
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