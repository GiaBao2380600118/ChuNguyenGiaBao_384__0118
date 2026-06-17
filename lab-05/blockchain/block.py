import hashlib
import json

class Block:
    def __init__(self, index, timestamp, transactions, proof, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Create a dictionary structure of the block
        block_dict = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "proof": self.proof,
            "previous_hash": self.previous_hash
        }
        # Dump block to a sorted JSON string and hash it
        block_string = json.dumps(block_dict, sort_keys=True).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def __repr__(self):
        return f"Block(Index: {self.index}, Hash: {self.hash[:10]}..., Proof: {self.proof})"
