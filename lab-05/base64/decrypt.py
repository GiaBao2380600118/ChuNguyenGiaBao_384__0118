import base64
import os

def main():
    if os.path.exists("base64_encoded.txt"):
        with open("base64_encoded.txt", "r") as f:
            encoded_str = f.read().strip()
        print(f"Read encoded text from base64_encoded.txt: {encoded_str}")
    else:
        encoded_str = input("Enter Base64 encoded string to decode: ")
        
    try:
        decoded_bytes = base64.b64decode(encoded_str.encode('utf-8'))
        decoded_str = decoded_bytes.decode('utf-8')
        print("Decoded Plaintext:", decoded_str)
    except Exception as e:
        print("Error decoding Base64:", e)

if __name__ == '__main__':
    main()
