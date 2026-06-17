import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad, unpad

HOST = '127.0.0.1'
PORT = 12345

# Generate Server's RSA Key Pair
print("Generating RSA key pair for Server...")
server_private_key = RSA.generate(2048)
server_public_key = server_private_key.publickey()
print("RSA Key pair generated.")

clients = {} # client_socket -> aes_key

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] Client {client_address} connected.")
    try:
        # Step 1: Send server's RSA public key to client
        pub_key_pem = server_public_key.export_key()
        client_socket.send(pub_key_pem)
        
        # Step 2: Receive the encrypted AES key from client
        encrypted_aes_key = client_socket.recv(256)
        if not encrypted_aes_key:
            return
        
        # Step 3: Decrypt AES key using Server's RSA private key
        cipher_rsa = PKCS1_OAEP.new(server_private_key)
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)
        clients[client_socket] = aes_key
        print(f"[KEY EXCHANGE] Shared AES key established with {client_address}.")

        # Step 4: Handle communication
        while True:
            # First 16 bytes is IV
            data = client_socket.recv(1024)
            if not data:
                break
            
            if len(data) < 16:
                continue

            iv = data[:16]
            ciphertext = data[16:]
            
            # Decrypt message
            cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
            decrypted_msg = unpad(cipher_aes.decrypt(ciphertext), AES.block_size).decode('utf-8')
            print(f"[{client_address}] (Decrypted): {decrypted_msg}")
            
            # Broadcast to all other clients
            broadcast(decrypted_msg, client_socket)

    except Exception as e:
        print(f"[ERROR] Connection with {client_address} lost: {e}")
    finally:
        if client_socket in clients:
            del clients[client_socket]
        client_socket.close()
        print(f"[DISCONNECTED] Client {client_address} disconnected.")

def broadcast(message, sender_socket):
    for client_socket, aes_key in clients.items():
        if client_socket != sender_socket:
            try:
                # Encrypt message with client's specific AES key
                cipher_aes = AES.new(aes_key, AES.MODE_CBC)
                iv = cipher_aes.iv
                encrypted_msg = cipher_aes.encrypt(pad(message.encode('utf-8'), AES.block_size))
                # Send IV + encrypted message
                client_socket.send(iv + encrypted_msg)
            except Exception as e:
                print(f"[BROADCAST ERROR] {e}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[STARTING] Server is listening on {HOST}:{PORT}")
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("[SHUTTING DOWN] Server shutting down.")
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()
