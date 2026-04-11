// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./SkillRegistryV3.sol";
import "./UnifiedReputation.sol";

contract SkillUpgradeGovernor {
    SkillRegistryV3 public registry;
    UnifiedReputation public reputation;

    struct UpgradeProposal {
        uint256 id;
        string skillId;
        bytes32 newCodeHash;
        uint256 totalWeight;
        bool executed;
    }

    mapping(uint256 => UpgradeProposal) public proposals;
    uint256 public proposalCount;

    constructor(address _registry, address _reputation) {
        registry = SkillRegistryV3(_registry);
        reputation = UnifiedReputation(_reputation);
    }

    function createProposal(string calldata skillId, bytes32 newCodeHash) external returns (uint256) {
        uint256 id = proposalCount++;
        proposals[id] = UpgradeProposal(id, skillId, newCodeHash, 0, false);
        return id;
    }

    function castVote(uint256 proposalId, bool support) external {
        UpgradeProposal storage p = proposals[proposalId];
        if (support) {
            (uint256 score,) = reputation.reputations(msg.sender);
            p.totalWeight += score;
        }
    }
}
