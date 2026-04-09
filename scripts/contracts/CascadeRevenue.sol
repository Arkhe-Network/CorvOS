// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title CascadeRevenue
 * @dev Recursively distributes royalties back to the root of a content lineage tree.
 * Hardened with ReentrancyGuard, Ownable, and Checks-Effects-Interactions.
 */
contract CascadeRevenue is ReentrancyGuard, Ownable {
    IERC20 public asiToken;
    uint256 public constant MAX_TREE_DEPTH = 10;

    struct ContributionNode {
        address payable contributor;
        uint16 royaltyBP; // Basis points (e.g., 500 = 5%)
        bytes32 parentHash;
        uint256 totalRevenueAccumulated;
        bool finalized;
    }

    mapping(bytes32 => ContributionNode) public tree;
    mapping(address => uint256) public pendingClaims;
    address public asiFoundation;

    event RevenueAdded(bytes32 indexed leafHash, uint256 amount);
    event RoyaltyClaimed(address indexed contributor, uint256 amount);

    constructor(address _asiToken, address _foundation) Ownable(msg.sender) {
        asiToken = IERC20(_asiToken);
        asiFoundation = _foundation;
    }

    function registerNode(bytes32 _contentHash, bytes32 _parentHash, address payable _contributor, uint16 _bp) external onlyOwner {
        require(!tree[_contentHash].finalized, "Node already exists");
        require(_bp <= 2000, "Royalty too high"); // Max 20% per node

        // Depth check to prevent DoS
        uint256 depth = 0;
        bytes32 current = _parentHash;
        while (current != 0x0) {
            depth++;
            require(depth <= MAX_TREE_DEPTH, "Max tree depth exceeded");
            current = tree[current].parentHash;
        }

        tree[_contentHash] = ContributionNode(_contributor, _bp, _parentHash, 0, true);
    }

    /**
     * @dev Distributes revenue from a leaf node upwards.
     */
    function distribute(bytes32 _leafHash, uint256 _amount) external nonReentrant {
        require(asiToken.transferFrom(msg.sender, address(this), _amount), "Transfer failed");

        bytes32 current = _leafHash;
        uint256 distributedSoFar = 0;

        while (current != 0x0) {
            ContributionNode storage node = tree[current];
            if (!node.finalized) break;

            uint256 share = (_amount * node.royaltyBP) / 10000;
            if (share > 0) {
                pendingClaims[node.contributor] += share;
                node.totalRevenueAccumulated += share;
                distributedSoFar += share;
            }
            current = node.parentHash;
        }

        uint256 foundationShare = _amount - distributedSoFar;
        if (foundationShare > 0) {
            pendingClaims[asiFoundation] += foundationShare;
        }

        emit RevenueAdded(_leafHash, _amount);
    }

    function claim() external nonReentrant {
        uint256 amount = pendingClaims[msg.sender];
        require(amount > 0, "Nothing to claim");

        // Effect
        pendingClaims[msg.sender] = 0;

        // Interaction
        require(asiToken.transfer(msg.sender, amount), "Payment failed");

        emit RoyaltyClaimed(msg.sender, amount);
    }
}
