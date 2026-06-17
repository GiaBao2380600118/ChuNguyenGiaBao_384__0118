import base64

def main():
    plaintext = input("Enter text to encode with Base64: ")
    encoded_bytes = base64.b64encode(plaintext.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8')
    print("Encoded Base64 result:", encoded_str)
    
    # Save the result to a file for decrypt.py to test
    with open("base64_encoded.txt", "w") as f:
        f.write(encoded_str)
    print("Saved encoded result to base64_encoded.txt")

if __name__ == '__main__':
    main()
