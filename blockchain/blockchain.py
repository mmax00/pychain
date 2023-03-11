from datetime import datetime
import hashlib
import json


class Block:
    def __init__(self, index, previous_hash) -> None:
        self.index = index
        self.timestamp = str(datetime.utcnow())
        self.previous_hash = previous_hash
        self.nonce = 0
        self.data = ""

    @property
    def as_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "proof": self.proof,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "data": self.data,
        }

    def compute_hash(self):
        endcoded_block = json.dumps(self.as_dict(), sort_keys=True).encode()
        return hashlib.sha256(endcoded_block).hexdigest()

    def proof_of_work(self, difficulty=4):
        is_proof = False

        while is_proof is False:
            hash = self.hash()

            if hash[:difficulty] == "0" * difficulty:
                is_proof = True
            else:
                self.nonce += 1

        return hash


class Blockchain:
    def __init__(self) -> None:
        self.chain = []
        self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof, previous_hash):
        new_block = Block(index=len(self.chain) + 1, proof=proof, previous_hash=previous_hash)
        self.chain.append(new_block)

    def get_last_block(self):
        return self.chain[-1]

    def is_valid_chain(self):
        previous_block = self.chain[0]

        for i in range(1, len(self.chain)):
            block = self.chain[i]

            if block.previous_hash != previous_block.hash():
                return False
