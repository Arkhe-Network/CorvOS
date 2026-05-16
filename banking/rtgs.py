import time
import hashlib

class RTGS:
    def __init__(self, phi_c_threshold=0.998):
        self.phi_c_threshold = phi_c_threshold
        self.settled_transactions = []

    def settle_real_time(self, sender, receiver, amount, phi_c):
        start_time = time.time()

        if phi_c < self.phi_c_threshold:
            return {"status": "rejected", "reason": "phi_c_too_low", "phi_c": phi_c}

        # Simulate processing time
        time.sleep(0.0125) # 12.5ms average settlement time mock
        end_time = time.time()

        tx_data = f"{sender}_{receiver}_{amount}_{start_time}"
        quantum_proof = f"QUANTUM_PROOF_{hashlib.sha3_256(tx_data.encode()).hexdigest()[:16]}"

        tx = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "phi_c": phi_c,
            "settlement_time_ms": (end_time - start_time) * 1000,
            "quantum_proof": quantum_proof,
            "status": "settled"
        }

        self.settled_transactions.append(tx)
        return tx
