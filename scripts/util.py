
from brownie import accounts, network, config, Contract 
from web3 import Web3

LOCAL_BLOCKCHAINS = ["development", "ganache-local", "mainnet-fork-dev"]
DECIMALS          = 8
# STARTING_PRICE    = Web3.toWei(2000, "ether")
STARTING_PRICE    = 200000000000


def get_account(index = None, id = None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAINS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

# contracts to mocks mapping 

contract_to_mock = {
                    # "eth_to_usd_price": MockV3Aggregator,
                    # "vrf_coordinator": VRFCoordinatorMock,
                    # "link_token": LinkToken, 
                   } 

def get_contract(contract_name: str):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAINS: #TODO: do not deploy mocks in fork 
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_addr = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_addr,
                                     contract_type.abi)
    return contract

def deploy_mocks(decimals = DECIMALS, starting_price = STARTING_PRICE):
    print("The active network is {}".format(network.show_active()))
    print("Deploying Mocks...")
    account = get_account()
    # MockV3Aggregator.deploy(decimals, starting_price, {"from": account})
    # link_token = LinkToken.deploy({"from": account})
    # VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Mocks deployed!")

def fund_with_link(contract_addr, account=None, link_token=None,
                   amount=100000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_addr, amount, {"from": account})
    tx.wait(1)
    print("Contract funded!")
    return tx


