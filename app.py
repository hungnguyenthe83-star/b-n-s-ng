a.metric("❤️ SINH LỰC", f'{st.session_state["hp"]}%')
b.metric("🏆 ĐIỂM SỐ", st.session_state["score"])
c.metric("👾 MỤC TIÊU", len(st.session_state["enemies"]))

hp = st.session_state["hp"]
st.markdown(f"""
<div style="height:10px;background:#18243e;border-radius:10px;overflow:hidden;
border:1px solid #34506d;margin:4px 0 18px">
<div style="width:{hp}%;height:100%;background:linear-gradient(90deg,#ff376f,#ffb347,#4dffe1);
box-shadow:0 0 14px #4dffe1;transition:width .4s"></div>
</div>
""", unsafe_allow_html=True)

# ===== BATTLEFIELD =====
st.markdown("### 🛰️ CHIẾN TRƯỜNG TÁC CHIẾN")
st.caption("🛸 Bạn · 👾 Kẻ địch · Mỗi hành động khiến địch di chuyển.")

player = st.session_state["player"]
enemies = st.session_state["enemies"]
cells = []

for r in range(SIZE):
    for c in range(SIZE):
        if [r, c] == player:
            cells.append('<div class="cell player"><span class="pulse"></span>🛸</div>')
        elif [r, c] in enemies:
            cells.append('<div class="cell enemy"><span class="enemy-icon">👾</span><span class="enemy-light"></span></div>')
        else:
            cells.append('<div class="cell empty"><span>·</span></div>')

# Build HTML separately and safely: avoid Python f-string parsing of CSS braces.
turn_number = int(st.session_state.get("turn", 1))
board_html = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width">
<style>
*{box-sizing:border-box}
body{margin:0;background:#070c1b;color:white;font-family:Arial,sans-serif}
.board{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:5px;
padding:10px;background:linear-gradient(135deg,#0e1932,#080d1b);
border:1px solid #24476c;border-radius:16px;box-shadow:0 0 25px #00d9ff18,inset 0 0 25px #152e53}
.cell{aspect-ratio:1;display:flex;align-items:center;justify-content:center;position:relative;
border-radius:8px;font-size:clamp(16px,3vw,28px);overflow:hidden}
.empty{background:#101a30;border:1px solid #17294a;color:#254468}
.empty span{animation:blink 2s infinite}
.player{background:radial-gradient(circle,#12485d,#0b213b);border:1px solid #48f4ff;
box-shadow:inset 0 0 15px #00eaff35;animation:spawn .35s ease-out}
.pulse{position:absolute;width:65%;height:65%;border:1px solid #4dfaff;border-radius:50%;animation:pulse 1.7s infinite}
.enemy{background:radial-gradient(circle,#541938,#20132d);border:1px solid #ff4d9d;
box-shadow:inset 0 0 15px #ff167544;animation:enemyGlow 1.2s infinite alternate}
.enemy-icon{z-index:2;animation:float 1.4s infinite ease-in-out}
.enemy-light{position:absolute;bottom:3px;width:45%;height:2px;background:#ff438d;box-shadow:0 0 8px #ff438d}
@keyframes pulse{0%{transform:scale(.5);opacity:1}100%{transform:scale(1.5);opacity:0}}
@keyframes enemyGlow{from{box-shadow:inset 0 0 5px #ff167522}to{box-shadow:inset 0 0 18px #ff167588}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
@keyframes blink{0%,100%{opacity:.3}50%{opacity:1}}
@keyframes spawn{from{transform:scale(.4);opacity:.3}to{transform:scale(1);opacity:1}}
.footer{color:#6f91bd;font-size:11px;letter-spacing:2px;margin:9px 2px}
</style></head><body>
<div class="board">""" + "".join(cells) + f"""
</div><div class="footer">SECTOR 08 // TURN {turn_number:03d} // NEURAL LINK ACTIVE</div>
</body></html>
"""

components.html(board_html, height=470, scrolling=False)

# ===== COMBAT LOG =====
effect = st.session_state["effect"]
accent = "#ff4d9d" if effect in ("damage", "warning") else "#53f7ff"
message = st.session_state["message"]
st.markdown(f"""
<div style="padding:13px 16px;border-radius:12px;background:linear-gradient(100deg,#101c35,#11152b);
border-left:4px solid {accent};box-shadow:0 0 16px #00cfff12;margin:12px 0">
<span style="color:#6b8db7;font-size:11px;letter-spacing:2px">COMBAT LOG</span><br>
<strong>{message}</strong>
</div>
""", unsafe_allow_html=True)

# ===== CONTROLS =====
st.markdown("### 🎮 BỘ ĐIỀU KHIỂN")
disabled = st.session_state["over"]
_, up, _ = st.columns(3)
left, down, right = st.columns(3)

if up.button("⬆️ TIẾN", use_container_width=True, disabled=disabled):
    move_player(-1, 0)
    st.rerun()

if left.button("⬅️ TRÁI", use_container_width=True, disabled=disabled):
    move_player(0, -1)
    st.rerun()

if down.button("⬇️ LÙI", use_container_width=True, disabled=disabled):
    move_player(1, 0)
    st.rerun()

if right.button("➡️ PHẢI", use_container_width=True, disabled=disabled):
    move_player(0, 1)
    st.rerun()

if st.button("⚡ FIRE — KHAI HỎA", type="primary",
              use_container_width=True, disabled=disabled):
    shoot()
    st.rerun()

if st.session_state["over"]:
    if st.session_state["hp"] <= 0:
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

