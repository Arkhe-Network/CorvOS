// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@layerzerolabs/solidity-examples/contracts/lzApp/NonblockingLzApp.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract UnifiedReputation is NonblockingLzApp, AccessControl {
    bytes32 public constant UPDATER_ROLE = keccak256("UPDATER_ROLE");

    struct Reputation {
        uint256 score;
        uint256 lastUpdated;
    }

    mapping(address => Reputation) public reputations;

    constructor(address _lzEndpoint) NonblockingLzApp(_lzEndpoint) {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(UPDATER_ROLE, msg.sender);
    }

    function broadcastReputationUpdate(address user, int256 delta, uint16 dstChainId) external payable onlyRole(UPDATER_ROLE) {
        bytes memory payload = abi.encode("REPUTATION_UPDATE", user, delta);
        _lzSend(dstChainId, payload, payable(msg.sender), address(0), bytes(""), msg.value);
    }

    function _nonblockingLzReceive(uint16 _srcChainId, bytes memory _srcAddress, uint64 _nonce, bytes memory _payload) internal override {
        (string memory action, address user, int256 delta) = abi.decode(_payload, (string, address, int256));
        if (keccak256(bytes(action)) == keccak256("REPUTATION_UPDATE")) {
            int256 newScore = int256(reputations[user].score) + delta;
            reputations[user].score = uint256(newScore >= 0 ? newScore : int256(0));
            reputations[user].lastUpdated = block.timestamp;
        }
    }
}
