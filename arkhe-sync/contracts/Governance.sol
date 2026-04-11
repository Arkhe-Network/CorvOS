// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IReputationOracle {
    function getVotingWeight(address user) external view returns (uint256);
}

contract Governance is AccessControl {
    bytes32 public constant PROPOSER_ROLE = keccak256("PROPOSER_ROLE");
    IReputationOracle public oracle;

    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        uint256 forVotes;
        uint256 againstVotes;
        bool executed;
    }

    Proposal[] public proposals;

    event ProposalCreated(uint256 indexed id, address proposer, string description);
    event VoteCast(uint256 indexed id, address voter, bool support, uint256 weight);

    constructor(address _oracle) {
        oracle = IReputationOracle(_oracle);
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(PROPOSER_ROLE, msg.sender);
    }

    function createProposal(string calldata description) external onlyRole(PROPOSER_ROLE) {
        uint256 id = proposals.length;
        proposals.push(Proposal(id, msg.sender, description, 0, 0, false));
        emit ProposalCreated(id, msg.sender, description);
    }

    function castVote(uint256 proposalId, bool support) external {
        Proposal storage p = proposals[proposalId];
        uint256 weight = oracle.getVotingWeight(msg.sender);
        if (support) p.forVotes += weight;
        else p.againstVotes += weight;
        emit VoteCast(proposalId, msg.sender, support, weight);
    }
}
