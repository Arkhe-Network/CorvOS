# Arkhe-Block Mainnet Migration Plan

## 1. Overview
The migration moves the Arkhe Horizon 2 infrastructure from Testnet simulation to a production-grade ZK-Rollup Mainnet anchored on Bitcoin via QSB.

## 2. Phases

### Phase 1: Security Hardening (Q3 2026)
- **Formal Verification:** Auditor review of `AsiReputation.sol` and `CascadeRevenue.sol`.
- **Slashing Stress Tests:** Simulate malicious agent behavior to ensure the VRO correctly penalizes bad actors.
- **ZK-Proof Integration:** Implement SNARK-based proofs for reputation vectors to ensure privacy while maintaining auditability.

### Phase 2: Liquidity & Seeding (Q4 2026)
- **ASIToken Genesis:** Official minting of the initial 1B ASI supply.
- **Liquidity Pools:** Establish ASI/BTC and ASI/ETH pools on decentralized exchanges.
- **Creator Onboarding:** Pilot program with 50 top human creators to register their content roots.

### Phase 3: Transition (Q1 2027)
- **State Migration:** Snapshotting Testnet DIDs and Reputation Vectors to Mainnet.
- **BFF Switchover:** Pointing production BFF instances to Mainnet RPC endpoints.
- **Bridge Activation:** Enable QSB-enabled cross-chain bridges for agent payouts.

## 3. Risk Mitigation
- **Halt Conditions:** Emergency pause functionality in all core contracts.
- **Oracle Redundancy:** Multiple independent VRO nodes to prevent single point of failure.
- **Gradual Rollout:** Revenue cascading enabled for 10% of content initially, scaling to 100% over 3 months.

---
**Timestamp:** 2026-04-10 | **Status:** DRAFT_V1
