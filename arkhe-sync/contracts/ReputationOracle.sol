// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./CoherenceToken.sol";

contract ReputationOracle is AccessControl {
    bytes32 public constant UPDATER_ROLE = keccak256("UPDATER_ROLE");
    bytes32 public constant SLASHER_ROLE = keccak256("SLASHER_ROLE");

    IERC20 public token;

    mapping(address => uint256) public reputationScore;
    mapping(address => uint256) public coherenceFactor;

    event ReputationUpdated(address indexed user, uint256 newReputation, int256 delta);
    event SlashingExecuted(address indexed user, uint256 reputationLost, uint256 tokensBurned);

    constructor(address _token) {
        token = IERC20(_token);
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    function updateReputation(address user, bool success) external onlyRole(UPDATER_ROLE) {
        if (success) {
            reputationScore[user] += 1e17;
            emit ReputationUpdated(user, reputationScore[user], 1e17);
        } else {
            uint256 lost = reputationScore[user] / 10;
            reputationScore[user] -= lost;
            emit SlashingExecuted(user, lost, 0);
        }
    }

    function getVotingWeight(address user) external view returns (uint256) {
        uint256 balance = token.balanceOf(user);
        uint256 reputation = reputationScore[user];
        return (balance * (1e18 + reputation)) / 1e18;
    }
}
