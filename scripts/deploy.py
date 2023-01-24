from brownie import accounts, config, Arbitrage, network 
from scripts.util import * 
import time


def deploy_arbitrage():
    account = get_account()
    arbitrage_contract = Arbitrage.deploy(
                                    config["networks"][network.show_active()]["sushiswap_v2_router"],
                                    config["networks"][network.show_active()]["uniswap_v2_router"],
                                    {"from":account},
                                    publish_source=config["networks"][network.show_active()].get("verify", False)
                                    )
                            
                                   
    print("Contract deployed {}".format(arbitrage_contract))
    return arbitrage_contract 
                            
def main():
    deploy_arbitrage()

