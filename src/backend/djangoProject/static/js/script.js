document.addEventListener('DOMContentLoaded', function() {
    // Get form elements by their IDs
    const scoreForm = document.getElementById('scoreForm');
    const gameId = parseInt(scoreForm.dataset.gameId, 10); // Parse as integer (base 10)

    // If the parsing fails and gameId is NaN, you can handle the error:
    if (isNaN(gameId)) {
        console.error('Invalid game ID');
        return;
    }
    const playerOneScoreInput = document.getElementById('playerOneScore');
    const playerTwoScoreInput = document.getElementById('playerTwoScore');
    const winnerSelect = document.getElementById('winner');
    const looserSelect = document.getElementById('looser');
    const submitButton = document.getElementById('submit_button');


    console.log({
        gameId,
        playerOneScoreInput,
        playerTwoScoreInput,
        winnerSelect,
        looserSelect,
        submitButton
    });

    // Add event listener to the submit button
    submitButton.addEventListener('click', function(event) {
        event.preventDefault();  // Prevent form submission to handle it with JavaScript

        // Collect values from the form
        const playerOneScore = parseInt(playerOneScoreInput.value);
        const playerTwoScore = parseInt(playerTwoScoreInput.value);
        const winnerId = winnerSelect.value;
        const looserId = looserSelect.value;

        // Construct the data object to send to the API
        const data = {
            game_id: gameId,
            player_one_score: playerOneScore,
            player_two_score: playerTwoScore,
            winner: winnerId,
            looser: looserId,
            is_completed: true
        };

        // API URL (replace with your actual API endpoint)
        const apiUrl = 'http://127.0.0.1:8000/api/score'; // Change this to your actual endpoint
        const csrfToken = getCookie('csrftoken');

        // Send the data to the API endpoint using fetch
        fetch(apiUrl, {
            method: 'POST',  // HTTP method
            headers: {
                'Content-Type': 'application/json',  // We are sending JSON data
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)  // Convert the data object to a JSON string
        })
        .then(response => response.json())  // Parse JSON response from the server
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                alert('Game updated successfully!');
                console.log('Updated game data:', data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Something went wrong while updating the game!');
        });
    });
});

// CSRF token helper (for Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}