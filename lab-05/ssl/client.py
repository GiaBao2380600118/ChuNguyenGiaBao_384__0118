import socket
import ssl

HOST = '127.0.0.1'
PORT = 12346

def main():
    # Setup SSL Context for client
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Wrap the socket
        ssl_socket = context.wrap_socket(raw_socket, server_hostname=HOST)
        ssl_socket.connect((HOST, PORT))
        print(f"[SSL CLIENT] Connected securely to server at {HOST}:{PORT}")
        
        while True:
            msg = input("Enter message to send (or 'exit' to quit): ")
            if msg.lower() == 'exit':
                break
            if not msg:
                continue
                
            ssl_socket.send(msg.encode('utf-8'))
            data = ssl_socket.recv(1024)
            print("[SSL CLIENT] Response:", data.decode('utf-8'))
            
    except ConnectionRefusedError:
        print("[SSL CLIENT] Error: Server is not running.")
    except Exception as e:
        print("[SSL CLIENT] Error:", e)
    finally:
        raw_socket.close()
        print("[SSL CLIENT] Connection closed.")

if __name__ == '__main__':
    main()
