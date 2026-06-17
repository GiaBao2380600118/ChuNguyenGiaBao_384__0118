import tornado.ioloop
import tornado.web
import tornado.websocket
import random
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii

PORT = 8888
AES_KEY = b'MySecretKeyForAES' # 16 bytes key

fruits = ["Apple", "Banana", "Cherry", "Durian", "Elderberry", "Fig", "Grape", "Honeydew"]
clients = set()

class FruitWebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("[WS SERVER] Client connected.")
        clients.add(self)

    def on_message(self, message):
        print(f"[WS SERVER] Received message from client: {message}")
        try:
            # Encrypt message with AES-CBC as per Câu 04
            cipher = AES.new(AES_KEY, AES.MODE_CBC)
            iv = cipher.iv
            padded_data = pad(message.encode('utf-8'), AES.block_size)
            ciphertext = cipher.encrypt(padded_data)
            
            response = {
                "type": "encrypted_response",
                "iv": binascii.hexlify(iv).decode('utf-8'),
                "ciphertext": binascii.hexlify(ciphertext).decode('utf-8')
            }
            self.write_message(json.dumps(response))
            print(f"[WS SERVER] Sent encrypted message back to client.")
        except Exception as e:
            print(f"[WS SERVER] Error encrypting: {e}")

    def on_close(self):
        print("[WS SERVER] Client disconnected.")
        clients.discard(self)

def send_fruit():
    if clients:
        fruit = random.choice(fruits)
        print(f"[WS SERVER] Streaming fruit: {fruit}")
        for client in clients:
            try:
                client.write_message(json.dumps({"type": "fruit", "data": fruit}))
            except Exception as e:
                print(f"[WS SERVER] Error sending to client: {e}")

def make_app():
    return tornado.web.Application([
        (r"/websocket", FruitWebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(PORT)
    print(f"[WS SERVER] Tornado WebSocket Server starting on ws://localhost:{PORT}/websocket")
    
    # Schedule sending fruit names every 3 seconds (3000 ms)
    tornado.ioloop.PeriodicCallback(send_fruit, 3000).start()
    
    tornado.ioloop.IOLoop.current().start()
