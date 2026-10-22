
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Dino Run",
    page_icon="🦖",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;900&display=swap');

.stApp {
    background: linear-gradient(#b8efff, #f4ffe1);
    font-family: 'Nunito', sans-serif;
    color: #24543c;
}
.block-container {
    max-width: 950px;
    padding-top: 2rem;
}
h1 {
    text-align: center;
    color: #237348;
    font-weight: 900;
}
div[data-testid="stMetric"] {
    background: #ffffffcc;
    border: 2px solid #9bdab2;
    border-radius: 14px;
    padding: 14px;
}
div[data-testid="stMetricValue"] {
    color: #237348;
    font-weight: 900;
}
.stButton button {
    width: 100%;
    min-height: 50px;
    background: #ffffff;
    color: #237348;
    border: 2px solid #58a977;
    border-radius: 12px;
    font-size: 18px;
    font-weight: 900;
}
.stButton button:hover {
    background: #e1ffe9;
    border-color: #ff9c45;
    color: #d36a23;
}
</style>
""", unsafe_allow_html=True)

# Khởi tạo game
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.best = 0
    st.session_state.turn = 0
    st.session_state.over = False
    st.session_state.obstacles = ["🌵", "🪨", "🌵", "🌵"]

def reset_game():
    st.session_state.score = 0
    st.session_state.turn = 0
    st.session_state.over = False
    st.session_state.obstacles = [
        random.choice(["🌵", "🪨"]),
        "🌵", "🪨", "🌵"
    ]

def play(jump):
    if st.session_state.over:
        return

    obstacles = st.session_state.obstacles
    hit = obstacles[0] in ["🌵", "🪨"]

    # Chướng ngại vật tiến về phía khủng long.
    st.session_state.obstacles = (
        obstacles[1:] +
        [random.choice(["🌵", "🌵", "🪨", "🌲"])]
    )

    st.session_state.turn += 1
    st.session_state.score += random.randint(5, 12)

    # Nhảy sẽ tránh được chướng ngại vật ở lượt này.
    if hit and not jump:
        st.session_state.over = True

    st.session_state.best = max(
        st.session_state.best,
        st.session_state.score
    )

# Tiêu đề
st.markdown("<h1>🦖 DINO RUN 🦖</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center'>"
    "CHẠY THẬT NHANH • NHẢY THẬT CAO • ĐỪNG ĐỤNG CÂY XƯƠNG RỒNG!"
    "</p>",
    unsafe_allow_html=True
)

# Bảng điểm
a, b, c = st.columns(3)
a.metric("🏁 ĐIỂM", st.session_state.score)
b.metric("🏆 KỶ LỤC", st.session_state.best)
c.metric("👣 LƯỢT CHẠY", st.session_state.turn)

# Sân chơi hoạt hình
scene = """
<div class="game">
    <div class="sun">☀️</div>
    <div class="cloud cloud1">☁️</div>
    <div class="cloud cloud2">☁️</div>
    <div class="mountain m1"></div>
    <div class="mountain m2"></div>
    <div class="dino">🦖</div>
    <div class="obstacles">""" + "　".join(
        st.session_state.obstacles
    ) + """</div>
    <div class="ground"></div>
    <div class="ground-line"></div>
    <div class="label">DINO WORLD • LEVEL 1</div>
</div>

<style>
.game {
    position: relative;
    height: 300px;
    overflow: hidden;
    border: 3px solid #79c59b;
    border-radius: 18px;
    background: linear-gradient(
        #9ce4ff 0%, #d9f8ff 67%,
        #eaffc8 67%, #eaffc8 100%
    );
    box-shadow: 0 7px 0 #a9d8b8;
}
.sun {
    position: absolute;
    top: 25px;
    right: 10%;
    font-size: 42px;
}
.cloud {
    position: absolute;
    font-size: 34px;
}
.cloud1 {top: 30px; left: 15%;}
.cloud2 {top: 85px; left: 62%;}
.mountain {
    position: absolute;
    bottom: 95px;
    width: 220px;
    height: 90px;
    border-radius: 100% 100% 0 0;
    background: #a5dfb2;
}
.m1 {left: -40px;}
.m2 {right: -50px; height: 70px; background: #86cf9b;}
.dino {
    position: absolute;
    left: 10%;
    bottom: 55px;
    font-size: 60px;
    z-index: 2;
    filter: drop-shadow(0 4px 0 #8bc79a);
}
.obstacles {
    position: absolute;
    left: 40%;
    right: 2%;
    bottom: 55px;
    font-size: 36px;
    white-space: nowrap;
    letter-spacing: 8px;
    z-index: 2;
}
.ground {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 52px;
    height: 5px;
    background: #4d9a63;
}
.ground-line {
    position: absolute;
    bottom: 25px;
    left: 0;
    color: #70b781;
    font-size: 25px;
    letter-spacing: 12px;
}
.label {
    position: absolute;
    top: 12px;
    left: 14px;
    font: bold 11px monospace;
    color: #34775b;
    letter-spacing: 2px;
}
</style>
"""

components.html(scene, height=320, scrolling=False)

# Điều khiển
if st.session_state.over:
    st.error("💥 GAME OVER! Khủng long đã va vào chướng ngại vật.")

    if st.button("🔄 CHƠI LẠI"):
        reset_game()
        st.rerun()
else:
    st.info(
        "Cách chơi: mỗi lần bấm là một bước. "
        "Bấm NHẢY để vượt qua vật cản!"
    )

    left, right = st.columns(2)

    with left:
        if st.button("🦘 NHẢY!"):
            play(jump=True)
            st.rerun()

    with right:
        if st.button("🏃 CHẠY TIẾP"):
            play(jump=False)
            st.rerun()

st.divider()
st.caption("🦖 DINO RUN • Python + Streamlit")
