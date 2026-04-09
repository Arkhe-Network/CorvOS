// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title CascadeMonetization
 * @dev Distributes revenue across contributor chains (Humans & Agents).
 */
contract CascadeMonetization {
    struct articleContribution {
        address humanAuthor;
        address researchAgent;
        address synthesisAgent;
        uint256 revenueTotal;
    }

    mapping(bytes32 => articleContribution) public articles;

    function distribute(bytes32 _articleId) external payable {
        articleContribution storage art = articles[_articleId];
        uint256 total = msg.value;

        // 40% Human Author
        uint256 authorPart = (total * 400) / 1000;
        // 30% Research Agent
        uint256 researchPart = (total * 300) / 1000;
        // 20% Synthesis Agent
        uint256 synthesisPart = (total * 200) / 1000;
        // 10% Protocol Fee
        uint256 protocolPart = total - (authorPart + researchPart + synthesisPart);

        payable(art.humanAuthor).transfer(authorPart);
        payable(art.researchAgent).transfer(researchPart);
        payable(art.synthesisAgent).transfer(synthesisPart);
        // Foundation fee remains in contract or sent to treasury
    }
}
