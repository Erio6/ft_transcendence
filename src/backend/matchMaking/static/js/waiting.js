function cancelMatchmaking() {
    console.log(home_url);
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ action: "cancel_matchmaking" }));
        socket.close();
    }
    window.location.href = home_url;
}

const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';

let cancelButton = document.getElementById("cancelButton");
cancelButton.addEventListener('click', cancelMatchmaking);


const socket = new WebSocket(wsProtocol + window.location.host + '/ws/matchmaking/' + matchID + '/');

socket.onopen = () => {
    console.log("Connected to matchmaking server: " + matchID);
};

socket.onclose = () => {
    console.log("Disconnected from matchmaking server: " + matchID);
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.action === 'game_ready') {
        window.location.href = data.game_url;
    }
};

document.addEventListener("page:unload", () => {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ action: "cancel_matchmaking" }));
        socket.close();
    }
});
