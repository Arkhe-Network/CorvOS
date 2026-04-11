// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./SkillReward.sol";
import "./Governance.sol";

contract OfflineBatchExecutor {
    SkillReward public skillReward;
    Governance public governance;

    constructor(address _skillReward, address _governance) {
        skillReward = SkillReward(_skillReward);
        governance = Governance(_governance);
    }

    struct SkillOp {
        uint8 opType; // 0=register, 1=purchase, 2=reportOutcome
        bytes data;
    }

    struct GovOp {
        uint8 opType; // 0=createProposal, 1=vote, 2=executeProposal
        bytes data;
    }

    function batchSkillOps(SkillOp[] calldata ops) external returns (bool[] memory results) {
        results = new bool[](ops.length);
        for (uint i = 0; i < ops.length; i++) {
            SkillOp memory op = ops[i];
            if (op.opType == 0) {
                (string memory skillId, uint256 price, bytes32 vkHash) = abi.decode(op.data, (string, uint256, bytes32));
                skillReward.registerSkill(skillId, price, vkHash);
                results[i] = true;
            } else if (op.opType == 1) {
                (string memory skillId) = abi.decode(op.data, (string));
                skillReward.purchaseSkill(skillId);
                results[i] = true;
            } else if (op.opType == 2) {
                (string memory skillId, bool success) = abi.decode(op.data, (string, bool));
                skillReward.reportOutcome(skillId, success);
                results[i] = true;
            } else {
                results[i] = false;
            }
        }
    }

    function batchGovOps(GovOp[] calldata ops) external returns (bool[] memory results) {
        results = new bool[](ops.length);
        for (uint i = 0; i < ops.length; i++) {
            GovOp memory op = ops[i];
            if (op.opType == 0) {
                (string memory description) = abi.decode(op.data, (string));
                governance.createProposal(description);
                results[i] = true;
            } else if (op.opType == 1) {
                (uint256 proposalId, bool support) = abi.decode(op.data, (uint256, bool));
                governance.castVote(proposalId, support);
                results[i] = true;
            } else {
                results[i] = false;
            }
        }
    }
}
