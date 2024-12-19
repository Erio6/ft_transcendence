// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import {Test, console} from "forge-std/Test.sol";
import {ScoreContract} from "../src/ScoreContract.sol";
import {DeployScoreContract} from "../script/DeployScoreContract.s.sol";

contract ScoreContractTest is Test {
    ScoreContract scoreContract;
    address USER = makeAddr("Elo");
    uint256 constant STARTING_VALUE = 10 ether;

    function setUp() public {
        DeployScoreContract deployScoreContract = new DeployScoreContract();
        scoreContract = deployScoreContract.run();
        vm.deal(USER, STARTING_VALUE);
    }

    function testRecordGameResult() public {
        string memory gameId = "game_1";
        string memory player1 = "jdoe";
        string memory player2 = "bsmith";
        uint256 score1 = 10;
        uint256 score2 = 5;

        vm.prank(msg.sender);
        console.log("Owner: ", msg.sender);
        console.log( "player1: ", player1);
        console.log( "player2: ", player2);
        scoreContract.recordGameResult(gameId, player1, player2, score1, score2);

        ScoreContract.GameResult memory result = scoreContract.getResult(gameId);
        console.log( "player1: ", result.player1);
        console.log( "player2: ", result.player2);
        assertEq(result.player1, player1, "Player 1 login mismatch");
        assertEq(result.player2, player2, "Player 2 login mismatch");
        assertEq(result.score1, score1, "Score 1 mismatch");
        assertEq(result.score2, score2, "Score 2 mismatch");
    }

    function testOnlyOwnerCanRecord() public {
        string memory gameId = "game_3";

        vm.prank(USER);
        vm.expectRevert("Only owner can call this function");
        scoreContract.recordGameResult(gameId, "player1", "player2", 10, 5);
    }

    function testCannotGetNonExistentGame() public {
        vm.expectRevert("Game not found");
        scoreContract.getResult("0");
    }
}