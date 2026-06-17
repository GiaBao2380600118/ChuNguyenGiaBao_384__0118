import hashlib

def main():
    test_str = "Gia Bao 0118"
    print(f"Hashing string: '{test_str}'")
    blake2b_hash = hashlib.blake2b(test_str.encode('utf-8')).hexdigest()
    blake2s_hash = hashlib.blake2s(test_str.encode('utf-8')).hexdigest()
    print("Blake2b Hash:", blake2b_hash)
    print("Blake2s Hash:", blake2s_hash)

if __name__ == '__main__':
    main()
