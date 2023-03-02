import random
import time

import requests

from nibiru import Msg, Network

import nibiru
from nibiru import Network
from multiprocessing import Process
import multiprocessing


def delegation(validator_address: str, mnemonic: str, amount: int):
    """Delegation to the corresponding validator
    amount 10_000_000 = 10 Nibi"""
    network = Network.incentivized_testnet(1)
    sdk = nibiru.Sdk.authorize(mnemonic).with_network(network)

    tx_resp = sdk.tx.execute_msgs(
        Msg.staking.delegate(
            delegator_address=sdk.address,
            validator_address=validator_address,  # get_validator_operator_address(sdk)
            amount=amount
        )
    )
    return tx_resp


def process_delegation(mnemonics: list):
    i = 0
    for mnemonic in mnemonics:
        i += 1
        print(multiprocessing.current_process().name, i, mnemonic)
        validator_address = "validator_address"
        amount = 1000000 * random.choice([6, 7, 8, 9, 10, 8, 9, 10, 11])
        try:
            x = delegation(validator_address, mnemonic, amount)
            print("success")
        except Exception as e:
            if "is smaller than" in str(e):
                print('Take next')
            else:
                print(e)
        time.sleep(0.5)


if __name__ == '__main__':
    file = open("mnemonic.txt", "r")
    all_lines = file.read().splitlines()

    processes = [
        Process(target=process_delegation, args=([all_lines]), name='proc_1'),
        # Process(target=process_delegation, args=([all_lines[500:1000]]), name='proc_2'),
        # Process(target=process_delegation, args=([all_lines[1000:1500]]), name='proc_3'),
        # Process(target=process_delegation, args=([all_lines[1500:2000]]), name='proc_4'),
        # Process(target=process_delegation, args=([all_lines[2000:2500]]), name='proc_5'),
    ]

    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()
