import hashlib

def main():
    test_str = "Gia Bao 0118"
    print(f"Hashing string: '{test_str}'")
    sha256_hash = hashlib.sha256(test_str.encode('utf-8')).hexdigest()
    print("SHA-256 Hash:", sha256_hash)

if __name__ == '__main__':
    main()
