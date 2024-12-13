const express = require("express");
const { Web3 } = require("web3");
const rpcURL = "http://127.0.0.1:8545"; // Example RPC URL/ Instantiate the provider
const web3 = new Web3(rpcURL); // Pass the provider to Web3

const ScoreContract = require("../artifacts/contracts/ScoreContract.sol/ScoreContract.json");
const contractABI = ScoreContract.abi;
const contractAddress = "0xf1796A4610C9b1cb11f1e9Fd4f78Ff197a0AD97F";// to update

const app = express();

web3.eth.net.isListening()
  .then(() => console.log("Web3 is connected"))
  .catch(err => console.error("Failed to connect:", err));

const contract = new web3.eth.Contract(contractABI, contractAddress);

app.use(express.json()); //middleware

//Get the score
app.get("/score", async (req, res) => {
  try {
    const score = await contract.methods.getScore("Elo").call();
    res.json({ score: score.toString() }); // Convert BigInt to string
  } catch (error) {
    console.error("Error fetching score:", error);
    res.status(500).json({ error: "Failed to fetch score" });
  }
});

app.post("/score", async (req, res) => {
  try {
    const { score } = req.body;
    const accounts = await web3.eth.getAccounts();
    const result = await contract.methods
        .setScore(score)
        .send({ from: accounts[0], gas: 500000 });

    // Convert BigInt to string for the response
    res.send(JSON.stringify({
        message: "Score set successfully",
        transaction: result
    }, (key, value) => (typeof value === "bigint" ? value.toString() : value)));
  } catch (error) {
    console.error("Error setting score:", error);
    res.status(500).json({ error: "Failed to set score" });
  }
});

app.listen(3000, () => {
  console.log("Server is running on port 3000");
});
