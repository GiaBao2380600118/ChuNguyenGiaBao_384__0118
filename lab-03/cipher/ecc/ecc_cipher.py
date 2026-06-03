import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

class ECCCipher:
    def __init__(self):
        self.keys_dir = os.path.join(os.path.dirname(__file__), "keys")
        os.makedirs(self.keys_dir, exist_ok=True)
        self.public_key_path = os.path.join(self.keys_dir, "publicKey.pem")
        self.private_key_path = os.path.join(self.keys_dir, "privateKey.pem")

    def generate_keys(self):
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()
        
        # Save private key to PEM
        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(self.private_key_path, "wb") as f:
            f.write(pem_private)
            
        # Save public key to PEM
        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(self.public_key_path, "wb") as f:
            f.write(pem_public)
            
        return "ECC Keys generated successfully"

    def load_keys(self):
        if not os.path.exists(self.public_key_path) or not os.path.exists(self.private_key_path):
            self.generate_keys()
            
        with open(self.private_key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )
            
        with open(self.public_key_path, "rb") as f:
            public_key = serialization.load_pem_public_key(
                f.read()
            )
            
        return private_key, public_key

    def sign(self, message, private_key):
        signature = private_key.sign(
            message.encode("utf-8"),
            ec.ECDSA(hashes.SHA256())
        )
        return signature

    def verify(self, message, signature, public_key):
        try:
            public_key.verify(
                signature,
                message.encode("utf-8"),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception:
            return False
