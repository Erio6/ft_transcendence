function cancelMatchmaking() {
    socket.close();
    window.location.href = "djangoProject:home";
}

const matchID = "{{ match_id }}";
const socket = new WebSocket('ws://' + window.location.host + '/ws/matchmaking/' + matchID + '/');

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
