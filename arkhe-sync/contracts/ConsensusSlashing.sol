// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@layerzerolabs/solidity-examples/contracts/lzApp/NonblockingLzApp.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "./UnifiedReputation.sol";

contract ConsensusSlashing is NonblockingLzApp, AccessControl {
    bytes32 public constant PROPOSER_ROLE = keccak256("PROPOSER_ROLE");
    bytes32 public constant VOTER_ROLE = keccak256("VOTER_ROLE");

    UnifiedReputation public unifiedReputation;

    struct Proposal {
        uint256 id;
        address target;
        uint256 penalty;
        uint256 totalVotes;
        bool executed;
    }

    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;

    constructor(address _lzEndpoint, address _unifiedReputation) NonblockingLzApp(_lzEndpoint) {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(PROPOSER_ROLE, msg.sender);
        _grantRole(VOTER_ROLE, msg.sender);
        unifiedReputation = UnifiedReputation(_unifiedReputation);
    }

    function createProposal(address target, uint256 penalty) external onlyRole(PROPOSER_ROLE) {
        uint256 id = proposalCount++;
        proposals[id] = Proposal(id, target, penalty, 0, false);
    }

    function vote(uint256 proposalId) external onlyRole(VOTER_ROLE) {
        Proposal storage p = proposals[proposalId];
        // Weight = reputation
        (uint256 score,) = unifiedReputation.reputations(msg.sender);
        p.totalVotes += score;
    }

    function _nonblockingLzReceive(uint16, bytes memory, uint64, bytes memory) internal override {
        // Handle cross-chain slashing commands
    }
}
