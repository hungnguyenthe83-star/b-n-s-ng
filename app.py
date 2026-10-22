
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="NEON SHOOTER",
    page_icon="⚡",
    layout="wide"
)

# ===== GIAO DIỆN NEON =====
st.markdown("""
<style>
.stApp {
    background:
      radial-gradient(ellipse at top, #14254b 0%, #080d1c 50%, #030610 100%);
    color: #eaf6ff;
}
header[data-testid="stHeader"] {background: transparent;}
h1 {
    color: #67f7ff !important;
    text-shadow: 0 0 12px #00d9ff, 0 0 35px #0077ff;
}
h2, h3 {color: #d8eaff !important;}
[data-testid="stMetric"] {
    background: linear-gradient(135deg,#101d37,#0a1024);
    border: 1px solid #245b83;
    border-radius: 15px;
    padding: 16px;
    box-shadow: 0 0 15px #00bfff18;
}
[data-testid="stMetricValue"] {color: #65f7ff;}
.stButton button {
    background: linear-gradient(135deg,#142b4e,#17203b);
    color: #8dfaff;
    border: 1px solid #38cde8;
    border-radius: 12px;
    min-height: 44px;
    font-weight: bold;
    transition: .2s;
}
.stButton button:hover {
    background: #174a67;
    color: white;
    border-color: #8dfaff;
    box-shadow: 0 0 18px #00d9ff65;
    transform: translateY(-2px);
}
hr {border-color:#233a5c;}
.small-note {color:#91a9cc;font-size:13px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
# ⚡ NEON SHOOTER
### `SURVIVAL PROTOCOL // 2088`
""")

SIZE = 8

def reset_game():
    st.session_state.player = [4, 4]
    st.session_state.enemies = [[0, 0], [0, 7], [7, 0], [7, 7]]
    st.session_state.hp = 100
    st.session_state.score = 0
    st.session_state.turn = 1
    st.session_state.message = "Hệ thống online. Tiêu diệt toàn bộ mục tiêu!"
    st.session_state.effect = "idle"
    st.session_state.over = False

if "player" not in st.session_state:
    reset_game()

def enemy_turn():
    if st.session_state.over:
        return

    p = st.session_state.player
    enemies = st.session_state.enemies
    damage = 0

    for e in enemies:
        distance = abs(e[0] - p[0]) + abs(e[1] - p[1])

        if distance <= 1:
            damage += 10
            continue

        if random.random() < 0.8:
            if abs(e[0] - p[0]) >= abs(e[1] - p[1]):
                e[0] += 1 if p[0] < e[0] else -1
            else:
                e[1] += 1 if p[1] < e[1] else -1

    st.session_state.hp = max(0, st.session_state.hp - damage)
    st.session_state.turn += 1

    if damage:
        st.session_state.message = f"⚠️ Bạn bị tấn công! Mất {damage} máu."
        st.session_state.effect = "damage"

    if st.session_state.hp <= 0:
        st.session_state.over = True
        st.session_state.message = "💀 TÍN HIỆU SINH TỒN ĐÃ MẤT!"
    elif not enemies:
        st.session_state.over = True
        st.session_state.message = "🏆 CHIẾN THẮNG! KHU VỰC ĐÃ AN TOÀN."

def move_player(dx, dy):
    if st.session_state.over:
        return

    p = st.session_state.player
    nx = max(0, min(SIZE - 1, p[0] + dx))
    ny = max(0, min(SIZE - 1, p[1] + dy))

    if [nx, ny] in st.session_state.enemies:
        st.session_state.message = "🚫 Có kẻ địch chắn đường!"
        st.session_state.effect = "warning"
        return

    p[0], p[1] = nx, ny
    st.session_state.message = "⚡ Di chuyển thành công."
    st.session_state.effect = "move"
    enemy_turn()

def shoot():
    if st.session_state.over:
        return

    p = st.session_state.player
    enemies = st.session_state.enemies

    if not enemies:
        return

    target = min(
        enemies,
        key=lambda e: abs(e[0] - p[0]) + abs(e[1] - p[1])
    )

    distance = abs(target[0] - p[0]) + abs(target[1] - p[1])

    if distance <= 3:
        enemies.remove(target)
        st.session_state.score += 100
        st.session_state.message = "💥 BÙM! Mục tiêu bị tiêu diệt! +100 điểm"
        st.session_state.effect = "hit"

        # Có cơ hội xuất hiện mục tiêu mới khi chơi lâu
        if random.random() < 0.35 and len(enemies) < 6:
            empty = [
                [r, c] for r in range(SIZE) for c in range(SIZE)
                if [r, c] != p and [r, c] not in enemies
                and abs(r - p[0]) + abs(c - p[1]) > 3
            ]
            if empty:
                enemies.append(random.choice(empty))
                st.session_state.message += "  👾 Phát hiện mục tiêu mới!"
    else:
        st.session_state.message = "🎯 Ngoài tầm bắn! Hãy đến gần hơn."
        st.session_state.effect = "warning"

    enemy_turn()

# ===== BẢNG THÔNG SỐ =====
a, b, c = st.columns(3)
a.metric("❤️ SINH LỰC", f"{st.session_state.hp}%")
b.metric("🏆 ĐIỂM SỐ", st.session_state.score)
c.metric("👾 MỤC TIÊU", len(st.session_state.enemies))

hp = st.session_state.hp
st.markdown(f"""
<div style="height:10px;background:#18243e;border-radius:10px;
overflow:hidden;border:1px solid #34506d;margin:4px 0 18px">
<div style="width:{hp}%;height:100%;
background:linear-gradient(90deg,#ff376f,#ffb347,#4dffe1);
box-shadow:0 0 14px #4dffe1;transition:width .4s"></div>
</div>
""", unsafe_allow_html=True)

# ===== CHIẾN TRƯỜNG =====
st.markdown("### 🛰️ CHIẾN TRƯỜNG TÁC CHIẾN")
st.caption("🟢 Bạn     🔴 Kẻ địch     · Mỗi hành động khiến địch di chuyển.")

p = st.session_state.player
enemies = st.session_state.enemies
cells = []

for r in range(SIZE):
    for c in range(SIZE):
        if [r, c] == p:
            cells.append("""
            <div class="cell player">
                <span class="pulse"></span>🛸
            </div>""")
        elif [r, c] in enemies:
            cells.append("""
            <div class="cell enemy">
                <span class="enemy-icon">👾</span>
                <span class="enemy-light"></span>
            </div>""")
        else:
            cells.append('<div class="cell empty"><span>·</span></div>')

board = "".join(cells)

board_html = f"""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width">
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#070c1b;color:white;font-family:Arial,sans-serif}}
.board{{
 display:grid;grid-template-columns:repeat(8,minmax(0,1fr));
 gap:5px;padding:10px;background:linear-gradient(135deg,#0e1932,#080d1b);
 border:1px solid #24476c;border-radius:16px;
 box-shadow:0 0 25px #00d9ff18,inset 0 0 25px #152e53;
}}
.cell{{
 aspect-ratio:1;display:flex;align-items:center;justify-content:center;
 position:relative;border-radius:8px;font-size:clamp(16px,3vw,28px);
 overflow:hidden;
}}
.empty{{background:#101a30;border:1px solid #17294a;color:#254468}}
.empty span{{animation:blink 2s infinite}}
.player{{
 background:radial-gradient(circle,#12485d,#0b213b);
 border:1px solid #48f4ff;box-shadow:inset 0 0 15px #00eaff35;
 animation:spawn .35s ease-out;
}}
.player .pulse{{
 position:absolute;width:65%;height:65%;border:1px solid #4dfaff;
 border-radius:50%;animation:pulse 1.7s infinite;
}}
.enemy{{
 background:radial-gradient(circle,#541938,#20132d);
 border:1px solid #ff4d9d;box-shadow:inset 0 0 15px #ff167544;
 animation:enemyGlow 1.2s infinite alternate;
}}
.enemy-icon{{z-index:2;animation:float 1.4s infinite ease-in-out}}
.enemy-light{{position:absolute;bottom:3px;width:45%;height:2px;
 background:#ff438d;box-shadow:0 0 8px #ff438d}}
@keyframes pulse{{0%{{transform:scale(.5);opacity:1}}100%{{transform:scale(1.5);opacity:0}}}}
@keyframes enemyGlow{{from{{box-shadow:inset 0 0 5px #ff167522}}to{{box-shadow:inset 0 0 18px #ff167588}}}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}
@keyframes blink{{0%,100%{{opacity:.3}}50%{{opacity:1}}}}
@keyframes spawn{{from{{transform:scale(.4);opacity:.3}}to{{transform:scale(1);opacity:1}}}}
.footer{{color:#6f91bd;font-size:11px;letter-spacing:2px;margin:9px 2px}}
</style></head><body>
<div class="board">{board}</div>
<div class="footer">SECTOR 08 // TURN {st.session_state.turn:03d} // NEURAL LINK ACTIVE</div>
</body></html>
"""

components.html(board_html, height=470, scrolling=False)

# ===== THÔNG BÁO =====
st.markdown(f"""
<div style="padding:13px 16px;border-radius:12px;
background:linear-gradient(100deg,#101c35,#11152b);
border-left:4px solid {'#ff4d9d' if st.session_state.effect in ['damage','warning'] else '#53f7ff'};
box-shadow:0 0 16px #00cfff12;margin:12px 0">
<span style="color:#6b8db7;font-size:11px;letter-spacing:2px">COMBAT LOG</span><br>
<strong>{st.session_state.message}</strong>
</div>
""", unsafe_allow_html=True)

# ===== BẢNG ĐIỀU KHIỂN =====
st.markdown("### 🎮 BỘ ĐIỀU KHIỂN")

_, up, _ = st.columns(3)
left, down, right = st.columns(3)

if up.button("⬆️ TIẾN", use_container_width=True):
    move_player(-1, 0)
    st.rerun()

if left.button("⬅️ TRÁI", use_container_width=True):
    move_player(0, -1)
    st.rerun()

if down.button("⬇️ LÙI", use_container_width=True):
    move_player(1, 0)
    st.rerun()

if right.button("➡️ PHẢI", use_container_width=True):
    move_player(0, 1)
    st.rerun()

st.markdown("")
if st.button("⚡ FIRE — KHAI HỎA", type="primary",
             use_container_width=True, disabled=st.session_state.over):
    shoot()
    st.rerun()

if st.session_state.over:
    if st.session_state.hp <= 0:
        st.error("💀 NHIỆM VỤ THẤT BẠI — Hệ thống đã ngừng hoạt động.")
    else:
        st.success("🏆 NHIỆM VỤ HOÀN THÀNH — Bạn là chiến binh huyền thoại!")

if st.button("🔄 RESTART — CHƠI LẠI", use_container_width=True):
    reset_game()
    st.rerun()

st.markdown("""
<hr>
<div style="text-align:center;color:#57789f;font-size:12px">
NEON CORPS © 2088 · POWERED BY PYTHON & STREAMLIT
</div>
""", unsafe_allow_html=True)

