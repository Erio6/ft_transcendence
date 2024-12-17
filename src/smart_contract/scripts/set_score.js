require('dotenv').config();
const { ethers } = require("ethers");
const ScoreContractABI = require("../artifacts/contracts/ScoreContract.sol/ScoreContract.json").abi;

async function main() {
  const playerName = "Elo";
  const score = 1;
  const contractAddress = process.env.CONTRACT_ADDRESS;

  const provider = new ethers.providers.JsonRpcProvider(process.env.RPC_URL);
  const signer = new ethers.Wallet(process.env.PRIVATE_KEY, provider )

  const contract = new ethers.Contract(contractAddress, ScoreContractABI, signer);

  const tx = await contract.setScore(playerName, score);
  console.log("Transaction hash:", tx.hash);
  await tx.wait();
  console.log("Score set successfully!");
}

main().catch(console.error);
