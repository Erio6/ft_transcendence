const left = document.querySelector('.left')
const right = document.querySelector('.right')
const ball = document.querySelector('.ball')
const line = document.querySelector('.line')
const line_v = document.querySelector('.line-v')
const line_v2 = document.querySelector('.line-v2')
const line_v3 = document.querySelector('.line-v3')
const game = document.querySelector('.game')
const left_score = document.querySelector('.score-left')
const right_score = document.querySelector('.score-right')

let ratio = 100;
let lastTimestamp = performance.now();
let ballData = {};
let paddleMoving = 0;
let paddleSpeed = 0;
let paddlePos = '';

const webSocket = new WebSocket("ws://localhost:12345");

let arrowDown = false;
let arrowUp = false;

let msg = {
    type: "move",
    data: "",
    value: false,
    loc: 0
}

webSocket.onopen = (event) => {
    console.log("WebSocket connection established.");
};

webSocket.onclose = (event) => {
    console.warn("WebSocket connection closed:", event);
    // Optionally attempt reconnection
};

webSocket.onerror = (error) => {
    console.error("WebSocket error:", error);
};

webSocket.onmessage = (event) => {
    console.log("message = " + event.data);
    const json = JSON.parse(event.data);
    if (json['type'] === 'paddle') {
        if (json['loc'] === 'left') {
            line_v.style["top"] = ((json['y']) * game.clientHeight / 100) + "px";
            left.style["top"] = ((json['y'] - (json['size'] / 2)) * game.clientHeight / 100) + "px";
        }
        else
            right.style["top"] = ((json['y'] - (json['size'] / 2)) * game.clientHeight / 100) + "px";
    }
    else if (json['type'] === 'ball') {
        setBall(json['x'], json['y'], json['v_x'], json['v_y'], json['speed']);
    }
    else if (json['type'] === 'init_ball') {
        ball.style["width"] = (json['radius'] * game.clientWidth / 100) + "px";
        ball.style["height"] = (json['radius'] * game.clientWidth / 100) + "px";
        setBall(json['x'], json['y'], json['v_x'], json['v_y'], json['speed']);
    }
    else if (json['type'] === 'init_paddle') {
        ratio = 100 + json['size'];
        if (json['loc'] === 'left') {
            left.style["left"] = (json['x'] * game.offsetWidth / 100) + "px";
            left.style["top"] = ((json['y'] - (json['size'] / 2)) * game.clientHeight / 100) + "px";
            left.style["height"] = (json['size'] * game.clientHeight / 100) + "px";
            left.style["width"] = (json['width'] * game.clientWidth / 100) + "px";
        }
        else {
            right.style["right"] = (json['x'] * game.offsetWidth / 100) + "px";
            right.style["top"] = ((json['y'] - (json['size'] / 2)) * game.clientHeight / 100) + "px";
            right.style["height"] = (json['size'] * game.clientHeight / 100) + "px";
            right.style["width"] = (json['width'] * game.clientWidth / 100) + "px";

        }
    }
    else if (json['type'] === 'client') {
        paddlePos = json['loc'];
        paddleSpeed = json['speed'];
    }
    else if (json['type'] === 'line') {
    }
    else if (json['type'] === 'score') {
        setBall(json['x'], json['y'], json['v_x'], json['v_y'], json['speed']);
        if (json['loc'] === 'left')
            left_score.textContent = json['value'];
        else if (json['loc'] === 'right')
            right_score.textContent = json['value'];
    }
    else if (json['type'] === 'debug') {
        line_v2.style['top'] = (json['line1'] * game.clientHeight / 100) + "px";
        line_v3.style['top'] = (json['line2'] * game.clientHeight / 100) + "px";
    }
}

addEventListener("keydown", (event) => {
    if (event.code === "ArrowDown" && !arrowDown) {
        paddleMoving = 1;
        msg.data = 1;
        msg.value = true;
        msg.loc = 0;
        webSocket.send(JSON.stringify(msg));
        arrowDown = true;
        console.log("down: true");
    }
    if (event.code === "ArrowUp" && !arrowUp) {
        paddleMoving = -1;
        msg.data = -1;
        msg.value = true;
        msg.loc = 1;
        webSocket.send(JSON.stringify(msg));
        arrowUp = true;
        console.log("up: true");
    }
});

addEventListener("keyup", (event) => {
    // console.log(event.code);
    if (event.code === "ArrowDown" && arrowDown) {
        paddleMoving = 0;
        msg.data = 0;
        msg.value = false;
        msg.loc = 0;
        webSocket.send(JSON.stringify(msg));
        arrowDown = false;
        console.log("down: false");
    }
    if (event.code === "ArrowUp" && arrowUp) {
        paddleMoving = 0;
        msg.data = 0;
        msg.value = false;
        msg.loc = 1;
        webSocket.send(JSON.stringify(msg));
        arrowUp = false;
        console.log("up: false");
    }
});

function moveBall(deltaTime) {
    ball.style["top"] = parseFloat(window.getComputedStyle(ball).top) + (ballData.v_y * ballData.speed * deltaTime * ((game.offsetHeight - parseFloat(window.getComputedStyle(ball).height)) / 100)) + "px";
    ball.style["left"] = parseFloat(window.getComputedStyle(ball).left) + (ballData.v_x * ballData.speed * deltaTime * ((game.offsetWidth - parseFloat(window.getComputedStyle(ball).height)) / 100)) + "px";
    if (ball.offsetTop < 0)
        ball.offsetTop = 0;
    else if (ball.offsetTop + ball.offsetWidth > game.offsetHeight)
        ball.offsetTop = game.offsetHeight - ball.offsetWidth;
    if (ball.offsetTop < 0 || ball.offsetTop + ball.offsetWidth > game.offsetHeight) {
        ballData.v_y *= -1;
    }
}

function setBall(x, y, v_x, v_y, speed) {
    ballData.x = x;
    ballData.y = y;
    ballData.v_x = v_x;
    ballData.v_y = v_y;
    ballData.speed = speed;
    ball.style["top"] = (y * (game.clientHeight - parseFloat(window.getComputedStyle(ball).width)) / 100) + "px";
    ball.style["left"] = (x * (game.offsetWidth - parseFloat(window.getComputedStyle(ball).width)) / 100) + "px";
}

function movePaddle(deltaTime) {
    if (paddlePos === 'left') {
        left.style['top'] = (parseFloat(window.getComputedStyle(left).top) + (paddleMoving * paddleSpeed * deltaTime * ((game.offsetHeight) / 100))) + "px";

        const halfHeight = left.offsetHeight / 2;
        if (left.offsetTop < 0)
            left.style['top'] = "0px";
        else if (left.offsetTop + left.offsetHeight > game.offsetHeight)
            left.style['top'] = (game.offsetHeight - left.offsetHeight) + "px";
    }
    else if (paddlePos === 'right') {
        right.style['top'] = (parseFloat(window.getComputedStyle(right).top) + (paddleMoving * paddleSpeed * deltaTime * ((game.offsetHeight) / 100))) + "px";

        const halfHeight = right.offsetHeight / 2;
        if (right.offsetTop < 0)
            right.style['top'] = "0px";
        else if (right.offsetTop + right.offsetHeight > game.offsetHeight)
            right.style['top'] = (game.offsetHeight - right.offsetHeight) + "px";
    }
}

function gameLoop(timestamp) {
    const deltaTime = (timestamp - lastTimestamp) / 1000;
    lastTimestamp = timestamp;

    movePaddle(deltaTime);
    moveBall(deltaTime);
    line.style["left"] = ((100 - 5.5) * (game.offsetWidth / 100)) + "px";


    requestAnimationFrame(gameLoop);
}

gameLoop(lastTimestamp);