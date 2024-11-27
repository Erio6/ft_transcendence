const left = document.querySelector('.left')
const right = document.querySelector('.right')
const game = document.querySelector('.game')

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
    if (json['loc'] === 'left')
        left.style["top"] = (json['y'] * game.clientHeight / 100) + "px";
    else
        right.style["top"] = (json['y'] * game.clientHeight / 100) + "px";

}

addEventListener("keydown", (event) => {
    if (event.code === "ArrowDown" && !arrowDown) {
        msg.data = 1;
        msg.value = true;
        msg.loc = 0;
        webSocket.send(JSON.stringify(msg));
        arrowDown = true;
        console.log("down: true");
    }
    if (event.code === "ArrowUp" && !arrowUp) {
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
        msg.data = 0;
        msg.value = false;
        msg.loc = 0;
        webSocket.send(JSON.stringify(msg));
        arrowDown = false;
        console.log("down: false");
    }
    if (event.code === "ArrowUp" && arrowUp) {
        msg.data = 0;
        msg.value = false;
        msg.loc = 1;
        webSocket.send(JSON.stringify(msg));
        arrowUp = false;
        console.log("up: false");
    }
});

function movePaddle(timestamp) {
    console.log("raf");
    if (arrowDown)
        console.log("down");
    if (arrowUp)
        console.log("up");
}
