// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract EntropyVote {
    struct Observer {
        uint256 coherenceScore;
        bool isAuthorized;
    }

    mapping(address => Observer) public observers;

    function vote(uint256 proposalId, bool support) external {
        require(observers[msg.sender].isAuthorized, "Not authorized");
        // Vote logic...
    }
}
