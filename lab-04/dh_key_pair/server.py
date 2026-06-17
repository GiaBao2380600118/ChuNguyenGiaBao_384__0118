import os
import time
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

def main():
    print("[SERVER] Generating Diffie-Hellman parameters (p, g)...")
    # Generate parameters (using 2048-bit key size for security)
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    
    print("[SERVER] Generating Server private and public keys...")
    server_private_key = parameters.generate_private_key()
    server_public_key = server_private_key.public_key()
    
    # Serialize and save parameters
    param_pem = parameters.parameter_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.ParameterFormat.PKCS3
    )
    with open("dh_parameters.pem", "wb") as f:
        f.write(param_pem)
        
    # Serialize and save server public key
    server_pub_pem = server_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open("server_public_key.pem", "wb") as f:
        f.write(server_pub_pem)
        
    print("[SERVER] Saved dh_parameters.pem and server_public_key.pem.")
    print("[SERVER] Waiting for client_public_key.pem...")
    
    # Remove old client public key and secret message if they exist
    if os.path.exists("client_public_key.pem"):
        os.remove("client_public_key.pem")
    if os.path.exists("secret_message.bin"):
        os.remove("secret_message.bin")

    # Wait for client's public key
    while not os.path.exists("client_public_key.pem"):
        time.sleep(0.5)
        
    print("[SERVER] client_public_key.pem detected. Reading...")
    time.sleep(0.1) # Small delay to ensure file is fully written
    
    with open("client_public_key.pem", "rb") as f:
        client_pub_pem = f.read()
        
    client_public_key = serialization.load_pem_public_key(client_pub_pem)
    
    # Compute shared secret
    shared_key = server_private_key.exchange(client_public_key)
    
    # Derive a symmetric key from the shared secret
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'dh handshake',
    ).derive(shared_key)
    
    secret_text = "DH-Key-Exchange-Success: Secure communication established!"
    print(f"[SERVER] Shared secret computed. Encrypting message: '{secret_text}'")
    
    # Encrypt the message using AES-GCM
    iv = os.urandom(12)
    encryptor = Cipher(
        algorithms.AES(derived_key),
        modes.GCM(iv),
    ).encryptor()
    
    ciphertext = encryptor.update(secret_text.encode('utf-8')) + encryptor.finalize()
    
    # Save IV, tag, and ciphertext
    with open("secret_message.bin", "wb") as f:
        f.write(iv + encryptor.tag + ciphertext)
        
    print("[SERVER] secret_message.bin written. Done.")

if __name__ == '__main__':
    main()
