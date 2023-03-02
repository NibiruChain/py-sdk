import socket
import time

import requests
import socks


def faucet(address):
    while True:
        headers = {
            'Content-type': 'multipart/form-data',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}

        x = requests.post(
            "https://faucet.itn-1.nibiru.fi/",
            json={
                "address": address,
                "coins": ["11000000unibi", "100000000unusd", "100000000uusdt"],
            }, verify=False, headers=headers

        )
        print(x.json())
        if x.status_code == 503:
            break
        if x.json()['status'] == 'success':
            print(1)
            break
        if x.json()['log'] == 'you can only request tokens once every 6h0m0s':
            print(2)
            break


if __name__ == '__main__':
    while True:
        with open("addresses.txt", "r") as f:
            i = 0
            all_addresses = f.read().splitlines()

            while len(all_addresses) > 0:

                addr = all_addresses.pop(0)
                i += 1
                print(addr, i)
                # Your proxy
                socks.set_default_proxy(socks.SOCKS5, "IP", port, True, 'login', 'pwd')
                socket.socket = socks.socksocket
                try:
                    faucet(addr)
                except Exception as e:
                    print('faucet', e)
                try:
                    x = requests.get('Link to proxy api')
                except Exception as e:
                    print('change proxy', e)
                if len(all_addresses) == 0:
                    break
                time.sleep(1)

