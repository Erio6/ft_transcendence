const { ethers } = require("hardhat");

async function main() {

    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);

    const ScoreContract = await ethers.getContractFactory("ScoreContract");
    const scoreContract = await ScoreContract.deploy();
    await scoreContract.waitForDeployment();

    console.log("ScoreContract deployed to:", scoreContract.address);
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
