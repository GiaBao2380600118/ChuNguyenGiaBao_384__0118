import hashlib

def main():
    test_str = "Gia Bao 0118"
    print(f"Hashing string: '{test_str}'")
    md5_hash = hashlib.md5(test_str.encode('utf-8')).hexdigest()
    print("MD5 Library Hash:", md5_hash)

if __name__ == '__main__':
    main()
