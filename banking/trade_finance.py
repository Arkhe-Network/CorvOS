import time
import hashlib

class TradeFinanceContract:
    STATES = ["DRAFT", "CONFIRMED", "SHIPPED", "DELIVERED", "SETTLED"]

    def __init__(self, parties, amount, terms, epsilon=1.0):
        self.contract_id = hashlib.sha3_256(f"{parties}{amount}{time.time()}".encode()).hexdigest()[:12]
        self.parties = parties
        self.amount = amount
        self.terms = terms
        self.state_idx = 0
        self.state = self.STATES[self.state_idx]
        self.pqc_signature = f"PQC_SIG_{self.contract_id}"
        self.epsilon = epsilon

    def advance_state(self):
        if self.state_idx < len(self.STATES) - 1:
            self.state_idx += 1
            self.state = self.STATES[self.state_idx]
            return True
        return False

    def get_status(self):
        return {
            "contract_id": self.contract_id,
            "state": self.state,
            "pqc_signature": self.pqc_signature,
            "differential_privacy_epsilon": self.epsilon
        }

class TradeFinanceManager:
    def __init__(self):
        self.contracts = []

    def create_contract(self, parties, amount, terms, epsilon=1.0):
        contract = TradeFinanceContract(parties, amount, terms, epsilon)
        self.contracts.append(contract)
        return contract

    def get_portfolio_summary(self):
        total_exposure = sum(c.amount for c in self.contracts if c.state != "SETTLED")
        return {
            "total_contracts": len(self.contracts),
            "total_exposure": total_exposure
        }
