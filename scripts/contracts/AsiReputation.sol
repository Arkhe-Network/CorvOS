// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title AsiReputation
 * @dev Manages vector-based reputation for Arkhe Agents.
 */
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title AsiReputation
 * @dev Manages vector-based reputation for Arkhe Agents.
 * Hardened with AccessControl and ReentrancyGuard.
 */
contract AsiReputation is AccessControl, ReentrancyGuard {
    bytes32 public constant ORACLE_ROLE = keccak256("ORACLE_ROLE");

    struct Agent {
        uint256 score; // 0-1000
        uint256 stake;
        bool isActive;
    }

    mapping(address => Agent) public agents;
    uint256 public constant MIN_STAKE = 1000 ether;

    event AgentSlashed(address indexed agent, uint256 penalty);

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    function registerAgent() external payable nonReentrant {
        require(msg.value >= MIN_STAKE, "Insufficient stake");
        require(!agents[msg.sender].isActive, "Already registered");
        agents[msg.sender] = Agent(500, msg.value, true);
    }

    function updateScore(address _agent, uint256 _newScore) external onlyRole(ORACLE_ROLE) {
        agents[_agent].score = _newScore;
    }

    function slash(address _agent, uint256 _penalty) external onlyRole(ORACLE_ROLE) nonReentrant {
        Agent storage a = agents[_agent];
        require(a.isActive, "Agent not active");
        uint256 penaltyAmount = (a.stake * _penalty) / 1000;
        a.stake -= penaltyAmount;
        a.score = a.score > (_penalty / 2) ? a.score - (_penalty / 2) : 0;
        emit AgentSlashed(_agent, penaltyAmount);
    }
}
