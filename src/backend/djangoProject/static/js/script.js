document.addEventListener('DOMContentLoaded', function() {
    // Get form elements by their IDs
    const gameIdInput = document.getElementById('game_id');
    const playerOneScoreInput = document.getElementById('player_one_score');
    const playerTwoScoreInput = document.getElementById('player_two_score');
    const winnerSelect = document.getElementById('winner');
    const looserSelect = document.getElementById('looser');
    const isCompletedInput = document.getElementById('is_completed');
    const submitButton = document.getElementById('submit_button');

    // Add event listener to the submit button
    submitButton.addEventListener('click', function(event) {
        event.preventDefault();  // Prevent form submission to handle it with JavaScript

        // Collect values from the form
        const gameId = gameIdInput.value;
        const playerOneScore = parseInt(playerOneScoreInput.value);
        const playerTwoScore = parseInt(playerTwoScoreInput.value);
        const winnerId = winnerSelect.value;
        const looserId = looserSelect.value;
        const isCompleted = isCompletedInput.checked;

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
        const apiUrl = 'http://127.0.0.1:8000/api/score';  // Change this to your actual endpoint

        // Send the data to the API endpoint using fetch
        fetch(apiUrl, {
            method: 'POST',  // HTTP method
            headers: {
                'Content-Type': 'application/json'  // We are sending JSON data
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