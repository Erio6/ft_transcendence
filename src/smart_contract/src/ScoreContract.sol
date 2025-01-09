pragma solidity ^0.8.0;

contract ScoreContract {

    struct GameResult {
        uint256 id;              // ID du jeu dans la base de données Django
        string player_one;       // username of player_one
        string player_two;       // username of  player_two
        uint256 player_one_score;
        uint256 player_two_score;
        uint256 timestamp;
    }

    // mapping of game id to game result;
    mapping(uint256 => GameResult) private gameResults;

    address public owner;

    //only the backend can interact with the smart contract
    constructor () {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    function recordGameResult(
        uint256 gameID,
        string memory player1,
        string memory player2,
        uint256 score1,
        uint256 score2
    ) external onlyOwner {
        require(bytes(player1).length > 0, "Player 1 must not be empty");
        require(bytes(player2).length > 0, "Player 2 must not be empty");
        gameResults[gameID] = GameResult({
            id: gameID,
            player_one: player1,
            player_two: player2,
            player_one_score: score1,
            player_two_score: score2,
            timestamp: block.timestamp
        });
    }

    function getResult(uint256 gameID) public view returns (GameResult memory) {
        require(gameResults[gameID].timestamp != 0, "Game not found");
        return gameResults[gameID];
    }
}