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

let lastTimestamp = performance.now();

let arrowDown = false;
let arrowUp = false;
let paddleMovingDown = 0, paddleMovingUp = 0;
let paddleSpeed = 0;
let paddlePos = '';
let paddleSize;
let leftY = game.offsetHeight / 2;
let rightY = game.offsetHeight / 2;
let ballPos = {
    x: 0,
    y: 0,
    v_x: 0,
    v_y: 0,
    speed: 0,
    radius: 0,
}
let lastPart = window.location.toString().split("/");
lastPart = lastPart.pop() || lastPart.pop();

const webSocket = new WebSocket("ws://localhost:8000/ws/game/" + lastPart + "/");

webSocket.onmessage = (event) => {
    console.log("message = " + event.data);
    const json = JSON.parse(event.data);
    if (json['type'] === 'paddle') {
        if (json['loc'] === 'left') {
            line_v.style["top"] = ((json['y']) * game.clientHeight / 100) + "px";
            leftY = json['y'] / 100 * game.offsetHeight;
            left.style.transform = `translate(${getTranslateXY(left).x}px, ${getTransformPos(leftY)})`;
        }
        else {
            rightY = json['y'] / 100 * game.offsetHeight;
            right.style.transform = `translate(${getTranslateXY(right).x}px, ${getTransformPos(rightY)})`;
        }
    }
    else if (json['type'] === 'ball') {
        ballPos.x = json['x'] * ((game.offsetWidth) / 100);
        ballPos.y = json['y'] * (game.offsetHeight / 100);
        ballPos.speed = json['speed'];
        ballPos.v_x = json['v_x'];
        ballPos.v_y = json['v_y'];
    }
    else if (json['type'] === 'init_ball') {
        ballPos.x = json['x'] * (game.offsetWidth / 100);
        ballPos.y = json['y'] * (game.offsetHeight / 100);
        ballPos.v_x = json['v_x'];
        ballPos.v_y = json['v_y'];
        ballPos.speed = json['speed'];
        ballPos.radius = json['radius'] * (game.offsetHeight / 100);
        ball.style["width"] = (ballPos.radius) + "px";
        ball.style["height"] = (ballPos.radius) + "px";
    }
    else if (json['type'] === 'init_paddle') {
        paddleSize = json['size'] * game.offsetHeight / 100;
        if (json['loc'] === 'left') {
            leftY = json['y'] / 100 * game.offsetHeight;
            left.style["height"] = (json['size'] * game.clientHeight / 100) + "px";
            left.style["width"] = (json['width'] * game.clientWidth / 100) + "px";
            left.style.transform = `translate(${json['x'] * game.offsetWidth / 100}px, ${getTransformPos(leftY)})`;
        }
        else {
            rightY = json['y'] / 100 * game.offsetHeight;
            right.style["height"] = (json['size'] * game.clientHeight / 100) + "px";
            right.style["width"] = (json['width'] * game.clientWidth / 100) + "px";
            right.style.transform = `translate(calc(${(100 - json['x']) * game.offsetWidth / 100}px - 100%), ${getTransformPos(rightY)})`;
        }
    }
    else if (json['type'] === 'client') {
        paddlePos = json['loc'];
        paddleSpeed = json['speed'];
    }
    else if (json['type'] === 'line') {
    }
    else if (json['type'] === 'score') {
        ballPos.x = json['x'] * (game.offsetWidth / 100);
        ballPos.y = json['y'] * (game.offsetHeight / 100);
        ballPos.speed = json['speed'];
        ballPos.v_x = json['v_x'];
        ballPos.v_y = json['v_y'];
        return;
        if (json['loc'] === 'left')
            right_score.textContent = json['value'];
        else if (json['loc'] === 'right')
            left_score.textContent = json['value'];
    }
    else if (json['type'] === 'debug') {
        line_v2.style['top'] = (json['line1'] * game.clientHeight / 100) + "px";
        line_v3.style['top'] = (json['line2'] * game.clientHeight / 100) + "px";
    }
}

addEventListener("keydown", (event) => {
    if (event.code === "ArrowDown" && !arrowDown) {
        paddleMovingDown = 1;
        webSocket.send(JSON.stringify({type: "move", data: 1, value: true}));
        arrowDown = true;
    }
    if (event.code === "ArrowUp" && !arrowUp) {
        paddleMovingUp = 1;
        webSocket.send(JSON.stringify({type: "move", data: -1, value: true}));
        arrowUp = true;
    }
});

addEventListener("keyup", (event) => {
    // console.log(event.code);
    if (event.code === "ArrowDown" && arrowDown) {
        paddleMovingDown = 0;
        webSocket.send(JSON.stringify({type: "move", data: 1, value: false}));
        arrowDown = false;
    }
    if (event.code === "ArrowUp" && arrowUp) {
        paddleMovingUp = 0;
        webSocket.send(JSON.stringify({type: "move", data: -1, value: false}));
        arrowUp = false;
    }
});

function getTranslateXY(element) {
    const style = window.getComputedStyle(element)
    const matrix = new DOMMatrixReadOnly(style.transform)
    return {
        x: matrix.m41,
        y: matrix.m42
    }
}

function getTransformPos(value) {
    return `calc(${value}px - 50%)`;
}

function movePaddle(deltaTime) {
    let paddleMoving = paddleMovingDown - paddleMovingUp;
    if (paddlePos === 'left') {
        const transformPos = getTranslateXY(left);
        leftY += (paddleMoving * paddleSpeed * deltaTime) * ((game.offsetHeight - paddleSize) / 100);
        if (leftY < paddleSize / 2)
            leftY = paddleSize / 2;
        else if (leftY > game.offsetHeight - paddleSize / 2)
            leftY = game.offsetHeight - paddleSize / 2;
        left.style.transform = `translate(${transformPos.x}px, ${getTransformPos(leftY)})`;
    }
    else if (paddlePos === 'right') {
        const transformPos = getTranslateXY(right);
        rightY += (paddleMoving * paddleSpeed * deltaTime) * ((game.offsetHeight - paddleSize / 2) / 100);
        if (rightY < paddleSize / 2)
            rightY = paddleSize / 2;
        else if (rightY > game.offsetHeight - paddleSize / 2)
            rightY = game.offsetHeight - paddleSize / 2;
        right.style.transform = `translate(${transformPos.x}px, ${getTransformPos(rightY)})`;
    }
}

function moveBall(deltaTime) {
    ballPos.x += ballPos.v_x * ballPos.speed * deltaTime * ((game.offsetWidth) / 100);
    ballPos.y += ballPos.v_y * ballPos.speed * deltaTime * (game.offsetHeight / 100);
    if (ballPos.y < ballPos.radius) {
        ballPos.y = ballPos.radius;
        ballPos.v_y *= -1;
    }
    else if (ballPos.y > game.offsetHeight - ballPos.radius / 2) {
        ballPos.y = game.offsetHeight - ballPos.radius / 2;
        ballPos.v_y *= -1;
    }
    ball.style.transform = `translate(${getTransformPos(ballPos.x)}, ${getTransformPos(ballPos.y)})`;
}

function gameLoop(timestamp) {
    const deltaTime = (timestamp - lastTimestamp) / 1000;
    lastTimestamp = timestamp;

    movePaddle(deltaTime);
    moveBall(deltaTime);
    // line.style["left"] = ((100 - 5.5) * (game.offsetWidth / 100)) + "px";

    requestAnimationFrame(gameLoop);
}

gameLoop(lastTimestamp);