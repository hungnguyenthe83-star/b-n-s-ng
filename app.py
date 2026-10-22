
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="NEON SHOOTER", page_icon="⚡", layout="wide")

# ===== NEON UI =====
st.markdown("""
<style>
.stApp {
    background: radial-gradient(ellipse at top, #14254b 0%, #080d1c 52%, #030610 100%);
    color: #eaf6ff;
}
header[data-testid="stHeader"] {background: transparent;}
h1 {color:#67f7ff !important;text-shadow:0 0 12px #00d9ff,0 0 30px #0077ff;}
h2,h3 {color:#d8eaff !important;}
[data-testid="stMetric"] {
    background:linear-gradient(135deg,#101d37,#0a1024);
    border:1px solid #245b83;border-radius:15px;padding:14px;
    box-shadow:0 0 15px #00bfff18;
}
[data-testid="stMetricValue"] {color:#65f7ff;}
.stButton button {
    background:linear-gradient(135deg,#142b4e,#17203b);
    color:#8dfaff;border:1px solid #38cde8;border-radius:12px;
    min-height:44px;font-weight:bold;transition:.2s;
}
.stButton button:hover {
    background:#174a67;color:white;border-color:#8dfaff;
    box-shadow:0 0 18px #00d9ff65;transform:translateY(-2px);
}
hr {border-color:#233a5c;}
</style>
""", unsafe_allow_html=True)

st.markdown("# ⚡ NEON SHOOTER")
st.caption("SURVIVAL PROTOCOL // 2088")

SIZE = 8

def reset_game():
    st.session_state["player"] = [4, 4]
    st.session_state["enemies"] = [[0, 0], [0, 7], [7, 0], [7, 7]]
    st.session_state["hp"] = 100
    st.session_state["score"] = 0
    st.session_state["turn"] = 1
    st.session_state["message"] = "Hệ thống online. Tiêu diệt toàn bộ mục tiêu!"
    st.session_state["effect"] = "idle"
    st.session_state["over"] = False

# Defensive initialization: supports fresh sessions and missing state keys.
if "player" not in st.session_state:
    reset_game()
else:
    defaults = {
        "enemies": [[0, 0], [0, 7], [7, 0], [7, 7]],
        "hp": 100, "score": 0, "turn": 1,
        "message": "Hệ thống online. Tiêu diệt toàn bộ mục tiêu!",
        "effect": "idle", "over": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def enemy_turn():
    if st.session_state["over"]:
        return

    player = st.session_state["player"]
    enemies = st.session_state["enemies"]
    damage = 0

    for enemy in enemies:
        distance = abs(enemy[0] - player[0]) + abs(enemy[1] - player[1])
        if distance <= 1:
            damage += 10
            continue

        if random.random() < 0.8:
            if abs(enemy[0] - player[0]) >= abs(enemy[1] - player[1]):
                enemy[0] += 1 if player[0] > enemy[0] else -1
            else:
                enemy[1] += 1 if player[1] > enemy[1] else -1

    st.session_state["hp"] = max(0, st.session_state["hp"] - damage)
    st.session_state["turn"] += 1

    if damage:
        st.session_state["message"] = f"⚠️ Bạn bị tấn công! Mất {damage} máu."
        st.session_state["effect"] = "damage"

    if st.session_state["hp"] <= 0:
        st.session_state["over"] = True
        st.session_state["message"] = "💀 TÍN HIỆU SINH TỒN ĐÃ MẤT!"
    elif not enemies:
        st.session_state["over"] = True
