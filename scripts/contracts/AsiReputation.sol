// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title AsiReputation
 * @dev Manages vector-based reputation for Arkhe Agents.
 */
contract AsiReputation {
    struct Agent {
        uint256 score; // 0-1000
        uint256 stake;
        bool isActive;
    }

    mapping(address => Agent) public agents;
    uint256 public constant MIN_STAKE = 1000 ether;

    event AgentSlashed(address indexed agent, uint256 penalty);

    function registerAgent() external payable {
        require(msg.value >= MIN_STAKE, "Insufficient stake");
        agents[msg.sender] = Agent(500, msg.value, true);
    }

    function updateScore(address _agent, uint256 _newScore) external {
        // Only designated Oracle can call this
        agents[_agent].score = _newScore;
    }

    function slash(address _agent, uint256 _penalty) external {
        Agent storage a = agents[_agent];
        uint256 penaltyAmount = (a.stake * _penalty) / 1000;
        a.stake -= penaltyAmount;
        a.score -= _penalty / 2;
        emit AgentSlashed(_agent, penaltyAmount);
    }
}
