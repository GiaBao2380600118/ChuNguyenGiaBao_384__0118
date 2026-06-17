import tornado.ioloop
import tornado.websocket
import json
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

URL = "ws://localhost:8888/websocket"
AES_KEY = b'MySecretKeyForAES' # Must match server's key

async def receive_messages(connection):
    while True:
        try:
            msg = await connection.read_message()
            if msg is None:
                print("\n[WS CLIENT] Connection closed by server.")
                break
            
            data = json.loads(msg)
            if data.get("type") == "fruit":
                print(f"\n[WS CLIENT] Received streamed fruit: {data['data']}")
            elif data.get("type") == "encrypted_response":
                iv = binascii.unhexlify(data['iv'])
                ciphertext = binascii.unhexlify(data['ciphertext'])
                cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
                decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
                print(f"\n[WS CLIENT] Received encrypted response from server.")
                print(f"  Ciphertext: {data['ciphertext']}")
                print(f"  Decrypted: {decrypted}")
                
            print("Enter message to send (or 'exit' to quit): ", end="", flush=True)
        except Exception as e:
            print(f"\n[WS CLIENT] Error: {e}")
            break

async def send_messages(connection):
    # Run in the main thread/loop to prompt user for input
    # Note: input() is blocking, so we run it in executor or simple loop
    while True:
        try:
            # We can run blocking input in a loop
            msg = await tornado.ioloop.IOLoop.current().run_in_executor(None, input, "Enter message to send (or 'exit' to quit): ")
            if msg.lower() == 'exit':
                connection.close()
                tornado.ioloop.IOLoop.current().stop()
                break
            if msg:
                await connection.write_message(msg)
        except Exception as e:
            print(f"[WS CLIENT] Send error: {e}")
            break

async def main():
    print(f"[WS CLIENT] Connecting to {URL}...")
    try:
        connection = await tornado.websocket.websocket_connect(URL)
        print("[WS CLIENT] Connected successfully.")
        
        # Start receive and send tasks
        tornado.ioloop.IOLoop.current().spawn_callback(receive_messages, connection)
        await send_messages(connection)
    except Exception as e:
        print(f"[WS CLIENT] Connection failed: {e}")
        tornado.ioloop.IOLoop.current().stop()

if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)
