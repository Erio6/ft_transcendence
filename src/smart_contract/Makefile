-include .env

deploy:; forge script script/DeployScoreContract.s.sol:DeployScoreContract --rpc-url http://localhost:8545 --private-key $(PRIVATE_KEY_ANVIL) --broadcast
deploy-sepolia:; forge script script/DeployScoreContract.s.sol:DeployScoreContract --rpc-url $(SEPOLIA_RPC_URL) --private-key $(PRIVATE_KEY) --broadcast --verify --etherscan-api-key $(ETHERSCAN_API_KEY) -vvvv