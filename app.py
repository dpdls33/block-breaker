import streamlit as st

st.set_page_config(page_title="Brick Breaker", layout="centered")

st.title("🎮 Streamlit Brick Breaker")
st.markdown("📱 스와이프로 바를 움직여 블럭을 부수세요")

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
canvas {
    background: #111;
    display: block;
    margin: auto;
    touch-action: none;
}
</style>
</head>
<body>

<canvas id="game" width="480" height="320"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// Ball
let x = canvas.width / 2;
let y = canvas.height - 30;
let dx = 2;
let dy = -2;
const ballRadius = 8;

// Paddle
const paddleHeight = 10;
const paddleWidth = 80;
let paddleX = (canvas.width - paddleWidth) / 2;

// Bricks
const brickRowCount = 4;
const brickColumnCount = 6;
const brickWidth = 60;
const brickHeight = 15;
const brickPadding = 10;
const brickOffsetTop = 30;
const brickOffsetLeft = 30;

let bricks = [];
for (let c = 0; c < brickColumnCount; c++) {
    bricks[c] = [];
    for (let r = 0; r < brickRowCount; r++) {
        bricks[c][r] = { x: 0, y: 0, status: 1 };
    }
}

// 🔥 터치 & 마우스 스와이프 처리
function movePaddle(clientX) {
    const rect = canvas.getBoundingClientRect();
    let xPos = clientX - rect.left;
    paddleX = xPos - paddleWidth / 2;

    if (paddleX < 0) paddleX = 0;
    if (paddleX > canvas.width - paddleWidth)
        paddleX = canvas.width - paddleWidth;
}

// 🔥 포인터 이벤트 (모바일 + PC 공통)
canvas.addEventListener("pointerdown", e => {
    movePaddle(e.clientX);
});

canvas.addEventListener("pointermove", e => {
    movePaddle(e.clientX);
});

// 충돌 판정
function collisionDetection() {
    for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {
            const b = bricks[c][r];
            if (b.status === 1) {
                if (
                    x > b.x &&
                    x < b.x + brickWidth &&
                    y > b.y &&
                    y < b.y + brickHeight
                ) {
                    dy = -dy;
                    b.status = 0;
                }
            }
        }
    }
}

function drawBall() {
    ctx.beginPath();
    ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = "#00ffff";
    ctx.fill();
    ctx.closePath();
}

function drawPaddle() {
    ctx.beginPath();
    ctx.rect(paddleX, canvas.height - paddleHeight, paddleWidth, paddleHeight);
    ctx.fillStyle = "#ffffff";
    ctx.fill();
    ctx.closePath();
}

function drawBricks() {
    for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {
            if (bricks[c][r].status === 1) {
                const brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
                const brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;
                ctx.beginPath();
                ctx.rect(brickX, brickY, brickWidth, brickHeight);
                ctx.fillStyle = "#ff6666";
                ctx.fill();
                ctx.closePath();
            }
        }
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBricks();
    drawBall();
    drawPaddle();
    collisionDetection();

    if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) dx = -dx;
    if (y + dy < ballRadius) dy = -dy;
    else if (y + dy > canvas.height - ballRadius) {
        if (x > paddleX && x < paddleX + paddleWidth) dy = -dy;
        else document.location.reload();
    }

    x += dx;
    y += dy;
    requestAnimationFrame(draw);
}

draw();
</script>
</body>
</html>
"""

st.components.v1.html(game_html, height=360)
