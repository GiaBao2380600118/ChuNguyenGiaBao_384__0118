import os
import time
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

def main():
    print("[CLIENT] Waiting for server_public_key.pem and dh_parameters.pem...")
    while not (os.path.exists("server_public_key.pem") and os.path.exists("dh_parameters.pem")):
        time.sleep(0.5)
        
    print("[CLIENT] Found server files. Reading...")
    time.sleep(0.1)
    
    with open("dh_parameters.pem", "rb") as f:
        param_pem = f.read()
    parameters = serialization.load_pem_parameters(param_pem)
    
    with open("server_public_key.pem", "rb") as f:
        server_pub_pem = f.read()
    server_public_key = serialization.load_pem_public_key(server_pub_pem)
    
    print("[CLIENT] Generating Client private and public keys...")
    client_private_key = parameters.generate_private_key()
    client_public_key = client_private_key.public_key()
    
    # Save client public key
    client_pub_pem = client_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open("client_public_key.pem", "wb") as f:
        f.write(client_pub_pem)
    print("[CLIENT] Saved client_public_key.pem.")
    
    # Compute shared secret
    shared_key = client_private_key.exchange(server_public_key)
    
    # Derive a symmetric key
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'dh handshake',
    ).derive(shared_key)
    
    print("[CLIENT] Shared secret computed. Waiting for secret_message.bin from server...")
    while not os.path.exists("secret_message.bin"):
        time.sleep(0.5)
        
    time.sleep(0.1)
    with open("secret_message.bin", "rb") as f:
        data = f.read()
        
    iv = data[:12]
    tag = data[12:28]
    ciphertext = data[28:]
    
    print("[CLIENT] Decrypting message...")
    decryptor = Cipher(
        algorithms.AES(derived_key),
        modes.GCM(iv, tag),
    ).decryptor()
    
    decrypted_msg = decryptor.update(ciphertext) + decryptor.finalize()
    print(f"[CLIENT] Decrypted secret message: {decrypted_msg.decode('utf-8')}")

if __name__ == '__main__':
    main()
