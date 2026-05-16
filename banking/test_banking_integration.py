import asyncio
from banking.core_settlement import CoreSettlementEngine, SettlementTransaction
from banking.fraud_detection import FraudDetectionEngine
from banking.compliance_automation import ComplianceAutomation
from banking.custody import QuantumCustody
from banking.rtgs import RTGSEngine
from banking.trade_finance import TradeFinanceContract

class MockPhiBus:
    async def get_global_coherence(self):
        return 0.9995

    async def request_consensus(self, topic, payload, min_approvals):
        return True

    async def publish_metric(self, name, value):
        pass

class MockTemporalChain:
    async def anchor_event(self, event_type, payload):
        return "mock_seal"

class MockHSM:
    async def sign(self, hash_val):
        return "mock_pqc_signature"

async def test_banking_services():
    print("Testing initialization of banking services...")

    phi_bus = MockPhiBus()
    temporal_chain = MockTemporalChain()
    hsm = MockHSM()

    print("1. Testing CoreSettlementEngine")
    settlement = CoreSettlementEngine(phi_bus, temporal_chain, hsm)
    txn = SettlementTransaction(
        txn_id="TXN-001",
        sender_bank="BANK_A",
        receiver_bank="BANK_B",
        amount=1000.0
    )
    res = await settlement.settle(txn)
    assert res is True
    assert txn.pqc_signature == "mock_pqc_signature"
    assert txn.temporal_seal == "mock_seal"

    print("2. Testing FraudDetectionEngine")
    fraud = FraudDetectionEngine(temporal_chain, phi_bus)

    # Fit the model with some dummy data before testing inference
    import numpy as np
    dummy_data = np.array([[1.0, 2.0], [1.1, 1.9], [0.9, 2.1], [10.0, 20.0]])
    fraud.model.fit(dummy_data)

    features = {"f1": 1.0, "f2": 2.0}
    score = await fraud.score_transaction(features)
    assert isinstance(score, float)

    print("3. Testing ComplianceAutomation")
    compliance = ComplianceAutomation(temporal_chain)
    seal = await compliance.generate_report("BACEN", "2026-Q1")
    assert seal == "mock_seal"

    print("4. Testing QuantumCustody")
    custody = QuantumCustody(hsm, temporal_chain)
    assert custody.hsm is hsm

    print("5. Testing RTGSEngine")
    rtgs = RTGSEngine(phi_bus)
    assert rtgs.qbus is phi_bus

    print("6. Testing TradeFinanceContract")
    trade = TradeFinanceContract(temporal_chain)
    assert trade.temporal is temporal_chain

    print("All tests passed.")

if __name__ == "__main__":
    asyncio.run(test_banking_services())