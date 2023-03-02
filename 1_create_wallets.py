import nibiru
from nibiru import wallet, Network
from multiprocessing import Process

def generate_wallet(iters, mnemonic_file, addresses_file):
    mnemonic_file = open(mnemonic_file, 'a')
    addresses_file = open(addresses_file, 'a')
    for i in range(iters):
        # Генерируем адрес
        mnemonic, private_key = wallet.PrivateKey.generate()
        # Записываем мнемонику
        mnemonic_file.write(mnemonic + '\n')
        # авторизация с нового адреса
        sdk = nibiru.Sdk.authorize(mnemonic).with_network(Network.incentivized_testnet(1))
        # Записываем адрес
        addresses_file.write(sdk.address + '\n')
        print(i+1, sdk.address)
    mnemonic_file.close()
    addresses_file.close()


if __name__ == '__main__':
    processes = [
        Process(target=generate_wallet, args=(3000, 'new_mnemonic_1.txt', 'new_addresses_1.txt')),
        # Process(target=generate_wallet, args=(500, 'new_mnemonic_2.txt', 'new_addresses_2.txt')),
        # Process(target=generate_wallet, args=(500, 'new_mnemonic_3.txt', 'new_addresses_3.txt')),
        # Process(target=generate_wallet, args=(500, 'new_mnemonic_4.txt', 'new_addresses_4.txt')),
    ]

    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()
