from blockchain import Blockchain
import json

def print_block(block):
    print(f"Block #{block.index}:")
    print(f"  Timestamp: {block.timestamp}")
    print(f"  Transactions: {json.dumps(block.transactions, indent=4)}")
    print(f"  Proof: {block.proof}")
    print(f"  Previous Hash: {block.previous_hash}")
    print(f"  Hash: {block.hash}")
    print("-" * 50)

def main():
    # Instantiate the Blockchain
    blockchain = Blockchain()

    # Print Genesis Block
    print_block(blockchain.chain[0])

    # Add transactions for Block 2
    blockchain.new_transaction(sender='Alice', recipient='Bob', amount=10)
    blockchain.new_transaction(sender='Bob', recipient='Charlie', amount=5)
    blockchain.new_transaction(sender='Charlie', recipient='Alice', amount=3)
    blockchain.new_transaction(sender='Genesis', recipient='Miner', amount=1)

    # Mine the next block
    last_block = blockchain.last_block
    last_proof = last_block.proof
    proof = blockchain.proof_of_work(last_proof)

    # Add the block to the chain
    block = blockchain.new_block(proof, previous_hash=last_block.hash)
    print_block(block)

    # Validate blockchain
    is_valid = blockchain.valid_chain(blockchain.chain)
    print(f"Is Blockchain Valid: {is_valid}")

if __name__ == '__main__':
    main()
