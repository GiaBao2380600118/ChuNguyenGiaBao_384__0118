import sys
import os

# Filter out local lab-03 directory from sys.path temporarily to import system rsa library
_original_path = sys.path[:]
sys.path = [p for p in sys.path if not p.endswith('lab-03') and not p.endswith('lab-03\\')]
import rsa
sys.path = _original_path


class RSACipher:
    def __init__(self):
        self.keys_dir = os.path.join(os.path.dirname(__file__), "keys")
        os.makedirs(self.keys_dir, exist_ok=True)
        self.public_key_path = os.path.join(self.keys_dir, "publicKey.pem")
        self.private_key_path = os.path.join(self.keys_dir, "privateKey.pem")

    def generate_keys(self):
        (pubkey, privkey) = rsa.newkeys(1024)
        with open(self.public_key_path, "wb") as f:
            f.write(pubkey.save_pkcs1())
        with open(self.private_key_path, "wb") as f:
            f.write(privkey.save_pkcs1())
        return "Keys generated successfully"

    def load_keys(self):
        if not os.path.exists(self.public_key_path) or not os.path.exists(self.private_key_path):
            self.generate_keys()
        
        with open(self.public_key_path, "rb") as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read())
        with open(self.private_key_path, "rb") as f:
            privkey = rsa.PrivateKey.load_pkcs1(f.read())
        return privkey, pubkey

    def encrypt(self, message, key):
        # Python-rsa requires a PublicKey to encrypt. 
        # If a PrivateKey is passed, we try to use its public counterpart or raise an error.
        if isinstance(key, rsa.PrivateKey):
            # In some academic contexts, they might try to "encrypt" with private key (which is signing).
            # But python-rsa strictly requires a PublicKey for encrypt.
            # We can construct a PublicKey from the PrivateKey's n and e.
            pubkey = rsa.PublicKey(key.n, key.e)
            return rsa.encrypt(message.encode("utf-8"), pubkey)
        return rsa.encrypt(message.encode("utf-8"), key)

    def decrypt(self, ciphertext, key):
        # Python-rsa requires a PrivateKey to decrypt.
        # If a PublicKey is passed, we raise an error.
        if isinstance(key, rsa.PublicKey):
            raise ValueError("Cannot decrypt with a Public Key in standard RSA.")
        return rsa.decrypt(ciphertext, key).decode("utf-8")

    def sign(self, message, key):
        # Key must be PrivateKey
        if isinstance(key, rsa.PublicKey):
            raise ValueError("Cannot sign with a Public Key.")
        return rsa.sign(message.encode("utf-8"), key, "SHA-256")

    def verify(self, message, signature, key):
        # Key must be PublicKey
        if isinstance(key, rsa.PrivateKey):
            # Convert private key to public key if needed
            key = rsa.PublicKey(key.n, key.e)
        try:
            rsa.verify(message.encode("utf-8"), signature, key)
            return True
        except rsa.VerificationError:
            return False
