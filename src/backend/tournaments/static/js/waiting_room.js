const playerList = document.getElementById('players_list');
console.log(tournamentID);
const ws = new WebSocket('ws://' + window.location.host + '/ws/tournaments/' + tournamentID + '/');

ws.onmessage = function (event) {
    const data = JSON.parse(event.data);
    console.log(data);

    if (data.type === 'tournament_update') {
        const players = data.players;
        const connectedCount = data.connected_count;
        const startButton = document.getElementById('start-button');

        if (data.ready_to_start && startButton) {
            startButton.style.display = 'block';
        } else if (startButton){
            startButton.style.display = 'none';
        }
        document.getElementById('connected-count').innerText = connectedCount;

        playerList.innerHTML = '';
        players.forEach(player => {
            const li = document.createElement('li');
            li.id = `player-${player.id}`;
            li.innerHTML = player.name;
            playerList.appendChild(li);
        });
    }

    if (data.event === 'player_leave') {
        console.log('Player left');
        updatePlayerList(data.players);
    }

    if (data.event === 'tournament_cancelled') {
        alert(data.message);
        window.location.href = data.tournament_home_url;
    }
}

function updatePlayerList(players) {
    playerList.innerHTML = '';
    players.forEach(player => {
        const li = document.createElement('li');
        li.id = `player-${player.id}`;
        li.innerHTML = player.name;
        playerList.appendChild(li);
    });
}

ws.onopen = function () {
    console.log('Connected to tournament server' + tournamentID);
}

ws.onclose = function () {
    console.log('Connection closed');
}
