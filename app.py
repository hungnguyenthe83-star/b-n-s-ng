
import streamlit as st
import random

st.set_page_config(page_title="Python Shooter", page_icon="🔫")

st.title("🔫 PYTHON SHOOTER")
st.caption("Di chuyển, tiêu diệt kẻ địch và cố gắng sống sót!")

SIZE = 8

def new_game():
    st.session_state.player = [4, 4]
    st.session_state.enemies = [
        [0, 0], [0, 7], [7, 0], [7, 7]
    ]
    st.session_state.hp = 100
    st.session_state.score = 0
    st.session_state.over = False

if "player" not in st.session_state:
    new_game()

def move_player(dx, dy):
    if st.session_state.over:
        return

    p = st.session_state.player
    nx = max(0, min(SIZE - 1, p[0] + dx))
    ny = max(0, min(SIZE - 1, p[1] + dy))

    if [nx, ny] not in st.session_state.enemies:
        p[0], p[1] = nx, ny

    enemy_turn()

def shoot():
    if st.session_state.over:
        return

    p = st.session_state.player
    enemies = st.session_state.enemies

    if enemies:
        target = min(
            enemies,
            key=lambda e: abs(e[0] - p[0]) + abs(e[1] - p[1])
        )

        distance = abs(target[0] - p[0]) + abs(target[1] - p[1])

        if distance <= 3:
            enemies.remove(target)
            st.session_state.score += 10
            st.toast("🎯 Bắn trúng! +10 điểm")
        else:
            st.toast("Kẻ địch quá xa! Hãy di chuyển lại gần.")

    enemy_turn()

def enemy_turn():
    if st.session_state.over:
        return

    p = st.session_state.player
    enemies = st.session_state.enemies

    for e in enemies:
        if abs(e[0] - p[0]) + abs(e[1] - p[1]) <= 1:
            st.session_state.hp -= 10
            continue

        if random.random() < 0.75:
            if e[0] != p[0]:
                e[0] += 1 if p[0] > e[0] else -1
            elif e[1] != p[1]:
                e[1] += 1 if p[1] > e[1] else -1

    st.session_state.hp = max(0, st.session_state.hp)

    if st.session_state.hp <= 0:
        st.session_state.over = True

    if not enemies:
        st.session_state.over = True

# Thông số
a, b, c = st.columns(3)
a.metric("❤️ Máu", st.session_state.hp)
b.metric("🏆 Điểm", st.session_state.score)
c.metric("👾 Kẻ địch", len(st.session_state.enemies))

st.progress(st.session_state.hp / 100)

# Bản đồ game
st.subheader("🗺️ Chiến trường")

p = st.session_state.player
enemies = st.session_state.enemies

for r in range(SIZE):
    cells = []
    for col in range(SIZE):
        if [r, col] == p:
            cells.append("🟢")
        elif [r, col] in enemies:
            cells.append("👾")
        else:
            cells.append("⬛")
    st.markdown("　".join(cells))

st.caption("🟢 Bạn · 👾 Kẻ địch · ⬛ Ô trống")

# Điều khiển
st.subheader("🎮 Điều khiển")

_, up, _ = st.columns(3)
left, down, right = st.columns(3)

if up.button("⬆️ Lên", use_container_width=True):
    move_player(-1, 0)

if left.button("⬅️ Trái", use_container_width=True):
    move_player(0, -1)

if down.button("⬇️ Xuống", use_container_width=True):
    move_player(1, 0)

if right.button("➡️ Phải", use_container_width=True):
    move_player(0, 1)

if st.button("🔫 BẮN!", use_container_width=True):
    shoot()

if st.session_state.over:
    if st.session_state.hp <= 0:
        st.error("💀 GAME OVER! Bạn đã hết máu.")
    else:
        st.success("🏆 CHIẾN THẮNG! Bạn đã tiêu diệt hết kẻ địch.")

if st.button("🔄 Chơi lại", use_container_width=True):
    new_game()
    st.rerun()

