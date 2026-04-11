// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract CrossChainSkillRegistry {
    address public localRegistry;

    constructor(address _localRegistry) {
        localRegistry = _localRegistry;
    }

    function sendSkillRegistration(uint16 dstChainId, string calldata skillId, uint256 price, bytes32 vkHash) external payable {
        // Simulation of LayerZero send
        println("Bridge: Sending skill registration to chain {}", dstChainId);
    }
}
