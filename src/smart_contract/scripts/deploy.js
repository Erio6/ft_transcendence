require('@nomicfoundation/hardhat-toolbox');
const hre = require("hardhat");

async function main() {
    // Retrieve the contract factory
    const ScoreContract = await hre.ethers.getContractFactory("ScoreContract");

    // Deploy the contract
    const scoreContract = await ScoreContract.deploy();

    // Ensure the deployment is complete
    await scoreContract.waitForDeployment();

    // Log the contract address
    console.log("ScoreContract deployed to:", scoreContract.address);
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
