import socket
import ssl
import threading

HOST = '127.0.0.1'
PORT = 12346

def handle_client(conn, addr):
    print(f"[SSL SERVER] Secure connection established with {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode('utf-8')
            print(f"[SSL SERVER] Received: {msg}")
            
            # Echo back message
            response = f"Server received: {msg}"
            conn.send(response.encode('utf-8'))
    except Exception as e:
        print(f"[SSL SERVER] Error with {addr}: {e}")
    finally:
        conn.close()
        print(f"[SSL SERVER] Connection with {addr} closed.")

def main():
    # Setup SSL Context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        certfile="certificates/server-cert.crt",
        keyfile="certificates/server-key.key"
    )
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[SSL SERVER] Listening on securely {HOST}:{PORT}")
    
    # Wrap the socket
    ssl_socket = context.wrap_socket(server_socket, server_side=True)
    
    try:
        while True:
            conn, addr = ssl_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("[SSL SERVER] Shutting down.")
    finally:
        ssl_socket.close()

if __name__ == '__main__':
    main()
