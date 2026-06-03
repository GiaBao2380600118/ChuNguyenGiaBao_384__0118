import os
import ecdsa

class ECCCipher:
    def __init__(self):
        self.keys_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "keys"))
        os.makedirs(self.keys_dir, exist_ok=True)
        self.public_key_path = os.path.join(self.keys_dir, "publicKey.pem")
        self.private_key_path = os.path.join(self.keys_dir, "privateKey.pem")

    def generate_keys(self):
        sk = ecdsa.SigningKey.generate() # Tạo khóa riêng tư
        vk = sk.get_verifying_key() # Lấy khóa công khai từ khóa riêng tư
        
        with open(self.private_key_path, "wb") as p:
            p.write(sk.to_pem())
            
        with open(self.public_key_path, "wb") as p:
            p.write(vk.to_pem())
            
        return "Keys generated successfully"
            
    def load_keys(self):
        if not os.path.exists(self.public_key_path) or not os.path.exists(self.private_key_path):
            self.generate_keys()
            
        with open(self.private_key_path, "rb") as p:
            sk = ecdsa.SigningKey.from_pem(p.read())
        with open(self.public_key_path, "rb") as p:
            vk = ecdsa.VerifyingKey.from_pem(p.read())
        return sk, vk

    def sign(self, message, key):
        # Ký dữ liệu bằng khóa riêng tư
        return key.sign(message.encode('ascii'))
        
    def verify(self, message, signature, key):
        vk = key
        try:
            return vk.verify(signature, message.encode('ascii'))
        except ecdsa.BadSignatureError:
            return False
