pragma solidity ^0.8.0;

contract ScoreContract {
    mapping(string => uint256) private scores;
    event ScoreUpdated(string playerName, uint256 score); // ENABLE FRONT END TO LISTEN FOR SCORE UPDATES using web3.js

    function setScore(string memory playerName, uint256 _score) public {
        require(bytes(playerName).length > 0, "Player name cannot be empty");
        scores[playerName] = _score;
        emit ScoreUpdated(playerName, _score);
    }

    function getScore(string memory playerName) public view returns (uint256) {
        return scores[playerName];
    }
}