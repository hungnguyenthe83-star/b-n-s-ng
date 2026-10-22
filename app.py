import streamlit as st
import streamlit.components.v1 as components

# Cấu hình giao diện trang Streamlit
st.set_page_config(
    page_title="Streamlit Dino Run", 
    page_icon="🦖", 
    layout="centered"
)

st.title("🦖 T-REX DINO RUN ON STREAMLIT")

# Bảng hướng dẫn chơi
st.markdown("""
<div style="background-color: rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; margin-bottom: 15px; font-size: 14px; text-align: center;">
    🕹️ Điều khiển: Bấm phím <strong>Mũi tên Lên (⬆)</strong> hoặc phím <strong>SPACE (Khoảng trắng)</strong> để nhảy né cây xương rồng!<br>
    <span style="color: #ff9f43; font-weight: bold;">💡 Mẹo: Nhấp chuột vào khung game một lần để kích hoạt bàn phím trước khi chơi.</span>
</div>
""", unsafe_allow_html=True)

# Toàn bộ mã nguồn Game (HTML/CSS/JS) độc lập, tránh lỗi f-string của Python
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background: #f7f7f7;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Courier New', Courier, monospace;
            flex-direction: column;
            padding: 10px;
            border-radius: 12px;
            overflow: hidden;
        }

        /* Bảng hiển thị điểm số phong cách retro */
        .score-container {
            display: flex;
            justify-content: flex-end;
            width: 700px;
            gap: 20px;
            font-size: 18px;
            font-weight: bold;
            color: #535353;
            margin-bottom: 10px;
        }

        .game-border {
            padding: 4px; background: #ddd; border-radius: 8px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.15); position: relative;
        }

        canvas {
            background: #ffffff;
            border-radius: 4px; outline: none;
        }

        .controls-btn { display: flex; gap: 15px; margin-top: 15px; }
        .btn {
            background: #535353; color: white; border: none; padding: 10px 22px;
            border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.15); transition: all 0.2s;
            font-family: inherit;
        }
        .btn:hover { background: #333; }
        
        .overlay {
            display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.05); color: #535353; font-size: 30px; font-weight: bold;
            justify-content: center; align-items: center; border-radius: 8px;
            pointer-events: none; flex-direction: column; gap: 10px;
        }
    </style>
</head>
<body>

    <!-- UI Điểm số -->
    <div class="score-container">
        <div>HI: <span id="highScore">00000</span></div>
        <div>SCORE: <span id="currentScore">00000</span></div>
    </div>

    <!-- Khung chứa canvas game -->
    <div class="game-border">
        <canvas id="gameCanvas" width="700" height="250" tabindex="1"></canvas>
        <div class="overlay" id="gameOverOverlay">G A M E  O V E R</div>
    </div>

    <!-- Nút tương tác -->
    <div class="controls-btn">
        <button class="btn" onclick="resetGame()">HỒI SINH TRẬN ĐẤU</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const overlay = document.getElementById("gameOverOverlay");

        canvas.focus();
        document.body.addEventListener("click", () => canvas.focus());

        let score = 0;
        let highScore = 0;
        let gameOver = false;
        let gameSpeed = 6;

        // Cấu hình Khủng long Dino
        const dinoWidth = 34;
        const dinoHeight = 40;
        let dino = {
            x: 50,
            y: 200 - dinoHeight,
            vy: 0,
            gravity: 0.6,
            jumpForce: -11,
            isJumping: false
        };

        // Cấu hình Chướng ngại vật (Xương rồng)
        let obstacles = [];
        let obstacleTimer = 0;

        // Hệ thống bắt phím bấm nhảy
        window.addEventListener("keydown", (e) => {
            if (e.key === "ArrowUp" || e.key === " " || e.key === "Spacebar") {
                e.preventDefault();
                if (!dino.isJumping && !gameOver) {
                    dino.vy = dino.jumpForce;
                    dino.isJumping = true;
                }
                if (gameOver) {
                    resetGame();
                }
            }
        });

        function formatScore(num) {
            return String(num).padStart(5, '0');
        }

        function spawnObstacle() {
            let type = Math.random() > 0.4 ? "single" : "double";
            let width = type === "single" ? 18 : 32;
            let height = Math.random() > 0.5 ? 35 : 45;
            
            obstacles.push({
                x: canvas.width,
                y: 200 - height,
                width: width,
                height: height
            });
        }

        function resetGame() {
            score = 0;
            gameSpeed = 6;
            obstacles = [];
            obstacleTimer = 0;
            dino.y = 200 - dinoHeight;
            dino.vy = 0;
            dino.isJumping = false;
            gameOver = false;
            overlay.style.display = "none";
            document.getElementById("currentScore").innerText = formatScore(score);
            canvas.focus();
        }

        function update() {
            if (gameOver) return;

            // Tăng điểm dần theo thời gian chạy
            score++;
            if (score % 100 === 0) {
                gameSpeed += 0.4; // Chạy càng xa tốc độ càng nhanh kịch tính
            }
            document.getElementById("currentScore").innerText = formatScore(score);

            // Xử lý Trọng lực vật lý cho Khủng long nhảy
            dino.vy += dino.gravity;
            dino.y += dino.vy;

            // Kiểm tra chạm đất sàn
            if (dino.y > 200 - dinoHeight) {
                dino.y = 200 - dinoHeight;
                dino.vy = 0;
                dino.isJumping = false;
            }

            // Quản lý sinh chướng ngại vật ngẫu nhiên khoảng cách
            obstacleTimer++;
            let minGap = Math.max(60, 110 - gameSpeed * 2);
            if (obstacleTimer > minGap + Math.random() * 50) {
                spawnObstacle();
                obstacleTimer = 0;
            }

            // Di chuyển và xử lý va chạm của xương rồng
            for (let i = obstacles.length - 1; i >= 0; i--) {
                let obs = obstacles[i];
                obs.x -= gameSpeed;

                // Xóa xương rồng đã chạy khuất màn hình bên trái
                if (obs.x + obs.width < 0) {
                    obstacles.splice(i, 1);
                    continue;
                }

                // Kiểm tra va chạm (Box Collision) giữa Dino và Xương rồng
                if (
                    dino.x < obs.x + obs.width &&
                    dino.x + dinoWidth > obs.x &&
                    dino.y < obs.y + obs.height &&
                    dino.y + dinoHeight > obs.y
                ) {
                    gameOver = true;
                    overlay.style.display = "flex";
                    if (score > highScore) {
                        highScore = score;
                        document.getElementById("highScore").innerText = formatScore(highScore);
                    }
                }
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Kẻ mặt đất phẳng chạy (Ground Line)
            ctx.strokeStyle = "#535353";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(0, 200);
            ctx.lineTo(canvas.width, 200);
            ctx.stroke();

            // 2. Vẽ Khủng long T-Rex (Dạng khối vuông phẳng Pixel nghệ thuật)
            ctx.fillStyle = "#535353";
            ctx.fillRect(dino.x, dino.y, dinoWidth, dinoHeight);
            
            // Vẽ mắt khủng long nhỏ đặc trưng
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(dino.x + 22, dino.y + 6, 4, 4);

            // 3. Vẽ các cây xương rồng (Obstacles) màu xám sẫm
            ctx.fillStyle = "#535353";
            obstacles.forEach(obs => {
                ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
            });
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        // Khởi động vòng lặp game lập tức
        gameLoop();
    </script>
</body>
</html>
"""

# Nhúng game HTML mượt mà vào Streamlit
components.html(game_html, height=400)
