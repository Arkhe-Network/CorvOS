// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface ICoherenceToken {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function mint(address to, uint256 amount) external returns (bool);
    function burn(address from, uint256 amount) external returns (bool);
}

contract SkillReward {
    address public token;

    struct Skill {
        string skillId;
        address author;
        uint256 price;
        uint256 successCount;
        uint256 failureCount;
        bytes32 verificationKeyHash;
        bool active;
    }

    mapping(string => Skill) public skills;
    mapping(address => uint256) public reputation;

    event SkillRegistered(string indexed skillId, address indexed author, uint256 price);
    event SkillPurchased(string indexed skillId, address indexed buyer, address indexed author, uint256 price);

    constructor(address _token) {
        token = _token;
    }

    function registerSkill(string calldata skillId, uint256 price, bytes32 vkHash) external {
        require(!skills[skillId].active, "Exists");
        skills[skillId] = Skill(skillId, msg.sender, price, 0, 0, vkHash, true);
        emit SkillRegistered(skillId, msg.sender, price);
    }

    function purchaseSkill(string calldata skillId) external {
        Skill storage s = skills[skillId];
        require(s.active, "Inactive");
        require(ICoherenceToken(token).transferFrom(msg.sender, s.author, s.price), "Failed");
        emit SkillPurchased(skillId, msg.sender, s.author, s.price);
    }

    function reportOutcome(string calldata skillId, bool success) external {
        Skill storage s = skills[skillId];
        if (success) {
            s.successCount++;
            uint256 reward = s.price / 10;
            ICoherenceToken(token).mint(s.author, reward);
            reputation[s.author] += reward;
        } else {
            s.failureCount++;
            uint256 penalty = s.price / 5;
            ICoherenceToken(token).burn(s.author, penalty);
            if (reputation[s.author] >= penalty) reputation[s.author] -= penalty;
        }
    }
}
