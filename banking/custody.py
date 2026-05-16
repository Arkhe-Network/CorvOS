import time

class QuantumSafeCustody:
    def __init__(self):
        self.vault = {}

    def deposit(self, asset_symbol, amount, owner_id):
        if asset_symbol not in self.vault:
            self.vault[asset_symbol] = []

        asset_record = {
            "amount": amount,
            "owner_id": owner_id,
            "hsm_key": f"HSM_KEY_{owner_id}_{int(time.time())}",
            "epr_witness": f"EPR_WITNESS_{asset_symbol}_{int(time.time())}"
        }

        self.vault[asset_symbol].append(asset_record)
        return asset_record

    def withdraw(self, asset_symbol, amount, owner_id):
        if asset_symbol not in self.vault:
            return {"status": "failed", "reason": "asset_not_found"}

        records = self.vault[asset_symbol]
        for idx, record in enumerate(records):
            if record["owner_id"] == owner_id and record["amount"] >= amount:
                # Mock withdrawal logic, simplify for test
                record["amount"] -= amount
                if record["amount"] == 0:
                    records.pop(idx)
                return {
                    "status": "success",
                    "withdrawn_amount": amount,
                    "hsm_verification": "verified",
                    "epr_witness": record["epr_witness"]
                }

        return {"status": "failed", "reason": "unauthorized_or_insufficient_funds"}
