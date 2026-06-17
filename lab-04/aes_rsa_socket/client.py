import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(client_socket, aes_key):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("\n[DISCONNECTED] Disconnected from server.")
                break
            
            if len(data) < 16:
                continue
            
            iv = data[:16]
            ciphertext = data[16:]
            
            cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
            decrypted_msg = unpad(cipher_aes.decrypt(ciphertext), AES.block_size).decode('utf-8')
            print(f"\nMessage received: {decrypted_msg}")
            print("Enter message to send: ", end="", flush=True)
        except Exception as e:
            print(f"\n[ERROR] Connection closed: {e}")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print("[CONNECTED] Connected to server.")
        
        # Step 1: Receive Server's RSA public key
        pub_key_pem = client_socket.recv(2048)
        server_public_key = RSA.import_key(pub_key_pem)
        print("[KEY EXCHANGE] Received Server's RSA Public Key.")
        
        # Step 2: Generate random 16-byte (128-bit) AES key
        aes_key = get_random_bytes(16)
        
        # Step 3: Encrypt AES key with Server's RSA public key
        cipher_rsa = PKCS1_OAEP.new(server_public_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        client_socket.send(encrypted_aes_key)
        print("[KEY EXCHANGE] Sent encrypted AES session key.")
        
        # Start receive thread
        recv_thread = threading.Thread(target=receive_messages, args=(client_socket, aes_key))
        recv_thread.daemon = True
        recv_thread.start()
        
        # Main thread handles sending messages
        while True:
            msg = input("Enter message to send: ")
            if msg.lower() == 'exit':
                break
            
            if not msg:
                continue
            
            # Encrypt message with AES
            cipher_aes = AES.new(aes_key, AES.MODE_CBC)
            iv = cipher_aes.iv
            encrypted_msg = cipher_aes.encrypt(pad(msg.encode('utf-8'), AES.block_size))
            
            # Send IV + encrypted message
            client_socket.send(iv + encrypted_msg)
            
    except ConnectionRefusedError:
        print("[ERROR] Server is not running.")
    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")
    finally:
        client_socket.close()

if __name__ == '__main__':
    main()
