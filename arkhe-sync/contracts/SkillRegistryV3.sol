// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "./UnifiedReputation.sol";

contract SkillRegistryV3 is AccessControl {
    bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");

    UnifiedReputation public reputation;

    struct SkillVersion {
        uint32 version;
        bytes32 codeHash;
        uint256 timestamp;
    }

    struct Skill {
        string skillId;
        address author;
        uint32 currentVersion;
        mapping(uint32 => SkillVersion) versions;
    }

    mapping(string => Skill) public skills;

    constructor(address _reputation) {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(UPGRADER_ROLE, msg.sender);
        reputation = UnifiedReputation(_reputation);
    }

    function registerSkill(string calldata skillId, bytes32 codeHash) external {
        Skill storage s = skills[skillId];
        s.skillId = skillId;
        s.author = msg.sender;
        s.currentVersion = 1;
        s.versions[1] = SkillVersion(1, codeHash, block.timestamp);
    }

    function upgradeSkill(string calldata skillId, bytes32 newCodeHash) external onlyRole(UPGRADER_ROLE) {
        Skill storage s = skills[skillId];
        s.currentVersion++;
        s.versions[s.currentVersion] = SkillVersion(s.currentVersion, newCodeHash, block.timestamp);
    }
}
