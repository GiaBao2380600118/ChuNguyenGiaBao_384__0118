import hashlib

def main():
    test_str = "Gia Bao 0118"
    print(f"Hashing string: '{test_str}'")
    # Using sha3_256
    sha3_hash = hashlib.sha3_256(test_str.encode('utf-8')).hexdigest()
    print("SHA-3 Hash:", sha3_hash)

if __name__ == '__main__':
    main()
