// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract MaterialSkillRegistry is AccessControl {
    bytes32 public constant EXPERIMENTER_ROLE = keccak256("EXPERIMENTER_ROLE");

    struct MaterialSkill {
        string skillId;
        address author;
        uint256 price;
        bytes32 circuitHash;
        bool active;
    }

    mapping(string => MaterialSkill) public skills;

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(EXPERIMENTER_ROLE, msg.sender);
    }

    function registerSkill(string calldata skillId, uint256 price, bytes32 circuitHash) external {
        require(!skills[skillId].active, "Exists");
        skills[skillId] = MaterialSkill(skillId, msg.sender, price, circuitHash, true);
    }
}
