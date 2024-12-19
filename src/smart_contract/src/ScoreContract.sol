pragma solidity ^0.8.0;

contract ScoreContract {

    struct GameResult {
        string player1;
        string player2;
        uint256 score1;
        uint256 score2;
        uint256 timestamp;
    }

    // mapping of game id to game result;
    mapping(string => GameResult) private gameResults;

    event ScoreUpdated(
        string indexed gameID,
        string player1,
        string player2,
        uint256 score1,
        uint256 score2);

    address public owner;

    //only the backend quand interact with the smart contract
    constructor () {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    function recordGameResult(
        string memory gameID,
        string memory player1,
        string memory player2,
        uint256 score1,
        uint256 score2
    ) external onlyOwner {
        require(score1 >= 0 && score2 >= 0, "Score must be positive");
        require(bytes(gameID).length > 0, "Game ID must not be empty");
        require(bytes(player1).length > 0, "Player 1 must not be empty");
        require(bytes(player2).length > 0, "Player 2 must not be empty");
        gameResults[gameID] = GameResult({
            player1: player1,
            player2: player2,
            score1: score1,
            score2: score2,
            timestamp: block.timestamp
        });
        emit ScoreUpdated(gameID, player1, player2, score1, score2);
    }

    function getResult(string memory gameID) public view returns (GameResult memory) {
        require(bytes(gameID).length > 0, "Game ID must not be empty");
        require(gameResults[gameID].timestamp != 0, "Game not found");
        return gameResults[gameID];
    }
}