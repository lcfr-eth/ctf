// SPDX-License-Identifier: MIT
pragma solidity ^0.8.15;

import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract Receiver is IERC721Receiver {
    address a = 0x328eBc7bb2ca4Bf4216863042a960E3C64Ed4c10;
    address v =  0xC357c220D9ffe0c23282fCc300627f14D9B6314C;

    function onERC721Received(
        address operator, 
        address from, 
        uint256 tokenId, 
        bytes calldata data
        ) external returns (bytes4) {
            IERC721(v).transferFrom(address(this), a, tokenId);
            return IERC721Receiver.onERC721Received.selector;
    } 
}
