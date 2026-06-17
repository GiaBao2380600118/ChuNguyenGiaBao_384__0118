import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPlainTextEdit, QPushButton, 
                             QMessageBox, QSplitter)
from PyQt5.QtCore import Qt
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

class ECCApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ECC Encryption & Decryption - Lab 06")
        self.resize(750, 600)
        self.init_ui()
        self.apply_premium_styling()
        self.load_keys_from_disk()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Title
        self.lbl_title = QLabel("ECC ENCRYPTION / DECRYPTION")
        self.lbl_title.setObjectName("lbl_title")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lbl_title)

        # Splitter to separate Keys section and Message section
        self.main_splitter = QSplitter(Qt.Vertical)
        self.layout.addWidget(self.main_splitter)

        # Top section: Key Generation & Keys display
        self.key_widget = QWidget()
        self.key_layout = QVBoxLayout(self.key_widget)
        self.key_layout.setContentsMargins(0, 0, 0, 0)
        
        self.btn_gen_keys = QPushButton("Generate ECC Key Pair (secp256r1)")
        self.btn_gen_keys.clicked.connect(self.handle_generate_keys)
        self.key_layout.addWidget(self.btn_gen_keys)

        self.keys_display_layout = QHBoxLayout()
        
        # Private Key Display
        self.priv_layout = QVBoxLayout()
        self.lbl_priv = QLabel("Private Key (PEM):")
        self.txt_private_key = QPlainTextEdit()
        self.txt_private_key.setPlaceholderText("Private key will appear here...")
        self.priv_layout.addWidget(self.lbl_priv)
        self.priv_layout.addWidget(self.txt_private_key)
        self.keys_display_layout.addLayout(self.priv_layout)

        # Public Key Display
        self.pub_layout = QVBoxLayout()
        self.lbl_pub = QLabel("Public Key (PEM):")
        self.txt_public_key = QPlainTextEdit()
        self.txt_public_key.setPlaceholderText("Public key will appear here...")
        self.pub_layout.addWidget(self.lbl_pub)
        self.pub_layout.addWidget(self.txt_public_key)
        self.keys_display_layout.addLayout(self.pub_layout)

        self.key_layout.addLayout(self.keys_display_layout)
        self.main_splitter.addWidget(self.key_widget)

        # Bottom section: Encryption / Decryption message fields
        self.crypto_widget = QWidget()
        self.crypto_layout = QVBoxLayout(self.crypto_widget)
        self.crypto_layout.setContentsMargins(0, 10, 0, 0)

        # Plaintext Display
        self.plain_layout = QVBoxLayout()
        self.lbl_plain = QLabel("Plain Text:")
        self.txt_plain_text = QPlainTextEdit()
        self.txt_plain_text.setPlaceholderText("Enter plaintext here...")
        self.plain_layout.addWidget(self.lbl_plain)
        self.plain_layout.addWidget(self.txt_plain_text)
        self.crypto_layout.addLayout(self.plain_layout)

        # Ciphertext Display
        self.cipher_layout = QVBoxLayout()
        self.lbl_cipher = QLabel("Cipher Text (Format: ephemeral_key:iv:tag:ciphertext in hex):")
        self.txt_cipher_text = QPlainTextEdit()
        self.txt_cipher_text.setPlaceholderText("Enter ciphertext format to decrypt, or view encrypted result here...")
        self.cipher_layout.addWidget(self.lbl_cipher)
        self.cipher_layout.addWidget(self.txt_cipher_text)
        self.crypto_layout.addLayout(self.cipher_layout)

        # Buttons
        self.btn_layout = QHBoxLayout()
        self.btn_encrypt = QPushButton("Encrypt with Public Key")
        self.btn_encrypt.clicked.connect(self.handle_encrypt)
        self.btn_layout.addWidget(self.btn_encrypt)

        self.btn_decrypt = QPushButton("Decrypt with Private Key")
        self.btn_decrypt.clicked.connect(self.handle_decrypt)
        self.btn_layout.addWidget(self.btn_decrypt)
        
        self.crypto_layout.addLayout(self.btn_layout)
        self.main_splitter.addWidget(self.crypto_widget)

    def apply_premium_styling(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121214;
            }
            QLabel {
                color: #E2E2E6;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
                font-weight: 500;
            }
            QLabel#lbl_title {
                color: #9089FC;
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 5px;
                letter-spacing: 1px;
            }
            QPlainTextEdit {
                background-color: #1A1A1E;
                color: #FFFFFF;
                border: 1px solid #2A2A32;
                border-radius: 8px;
                padding: 8px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
            }
            QPlainTextEdit:focus {
                border: 1px solid #9089FC;
            }
            QPushButton {
                background-color: #9089FC;
                color: #121214;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #A59FFA;
            }
            QPushButton:pressed {
                background-color: #7B73F0;
            }
        """)

    def load_keys_from_disk(self):
        keys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys")
        priv_path = os.path.join(keys_dir, "privateKey.pem")
        pub_path = os.path.join(keys_dir, "publicKey.pem")
        if os.path.exists(priv_path) and os.path.exists(pub_path):
            try:
                with open(priv_path, "r", encoding="utf-8") as f:
                    priv_pem = f.read()
                with open(pub_path, "r", encoding="utf-8") as f:
                    pub_pem = f.read()
                self.txt_private_key.setPlainText(priv_pem)
                self.txt_public_key.setPlainText(pub_pem)
            except Exception:
                pass

    def handle_generate_keys(self):
        try:
            private_key = ec.generate_private_key(ec.SECP256R1())
            public_key = private_key.public_key()
            
            # Serialize
            priv_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')
            
            pub_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
            
            # Save to keys folder
            keys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys")
            os.makedirs(keys_dir, exist_ok=True)
            with open(os.path.join(keys_dir, "privateKey.pem"), "w", encoding="utf-8") as f:
                f.write(priv_pem)
            with open(os.path.join(keys_dir, "publicKey.pem"), "w", encoding="utf-8") as f:
                f.write(pub_pem)

            self.txt_private_key.setPlainText(priv_pem)
            self.txt_public_key.setPlainText(pub_pem)
            QMessageBox.information(self, "Success", "ECC Key Pair generated successfully and saved to disk!")
        except Exception as e:
            QMessageBox.critical(self, "Key Gen Error", f"Failed to generate keys: {str(e)}")

    def handle_encrypt(self):
        pub_pem_str = self.txt_public_key.toPlainText().strip()
        plaintext = self.txt_plain_text.toPlainText()
        
        if not pub_pem_str:
            QMessageBox.warning(self, "Input Error", "Please provide a valid Public Key in PEM format.")
            return
        if not plaintext:
            QMessageBox.warning(self, "Input Error", "Plaintext cannot be empty.")
            return
            
        try:
            # Load public key
            public_key = serialization.load_pem_public_key(pub_pem_str.encode('utf-8'))
            if not isinstance(public_key, ec.EllipticCurvePublicKey):
                raise ValueError("Provided key is not an Elliptic Curve Public Key")

            # 1. Generate ephemeral key
            ephemeral_private = ec.generate_private_key(ec.SECP256R1())
            ephemeral_public = ephemeral_private.public_key()

            # 2. Derive shared key
            shared_secret = ephemeral_private.exchange(ec.ECDH(), public_key)

            # 3. KDF
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'ecc-encryption',
            ).derive(shared_secret)

            # 4. Encrypt with AES-GCM
            iv = os.urandom(12)
            encryptor = Cipher(algorithms.AES(derived_key), modes.GCM(iv)).encryptor()
            ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
            tag = encryptor.tag

            # 5. Serialize ephemeral public key
            eph_pub_pem = ephemeral_public.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            # Formatted transport string
            formatted_ciphertext = f"{eph_pub_pem.hex()}:{iv.hex()}:{tag.hex()}:{ciphertext.hex()}"
            self.txt_cipher_text.setPlainText(formatted_ciphertext)
            QMessageBox.information(self, "Success", "Encrypted Successfully using ECIES!")
        except Exception as e:
            QMessageBox.critical(self, "Encryption Error", f"Failed to encrypt: {str(e)}")

    def handle_decrypt(self):
        priv_pem_str = self.txt_private_key.toPlainText().strip()
        ciphertext_str = self.txt_cipher_text.toPlainText().strip()
        
        if not priv_pem_str:
            QMessageBox.warning(self, "Input Error", "Please provide a valid Private Key in PEM format.")
            return
        if not ciphertext_str:
            QMessageBox.warning(self, "Input Error", "Ciphertext cannot be empty.")
            return
            
        try:
            # Parse components
            parts = ciphertext_str.split(':')
            if len(parts) != 4:
                raise ValueError("Ciphertext format is invalid. Must be 'ephemeral_key:iv:tag:ciphertext' in hex format.")
                
            eph_pub_pem = bytes.fromhex(parts[0])
            iv = bytes.fromhex(parts[1])
            tag = bytes.fromhex(parts[2])
            ciphertext = bytes.fromhex(parts[3])

            # Load private key
            private_key = serialization.load_pem_private_key(priv_pem_str.encode('utf-8'), password=None)
            if not isinstance(private_key, ec.EllipticCurvePrivateKey):
                raise ValueError("Provided key is not an Elliptic Curve Private Key")

            # Load ephemeral public key
            ephemeral_public = serialization.load_pem_public_key(eph_pub_pem)

            # Derive shared secret
            shared_secret = private_key.exchange(ec.ECDH(), ephemeral_public)

            # Derive AES key
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'ecc-encryption',
            ).derive(shared_secret)

            # Decrypt AES-GCM
            decryptor = Cipher(algorithms.AES(derived_key), modes.GCM(iv, tag)).decryptor()
            decrypted_bytes = decryptor.update(ciphertext) + decryptor.finalize()

            self.txt_plain_text.setPlainText(decrypted_bytes.decode('utf-8'))
            QMessageBox.information(self, "Success", "Decrypted Successfully using ECIES!")
        except Exception as e:
            QMessageBox.critical(self, "Decryption Error", f"Failed to decrypt: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ECCApp()
    window.show()
    sys.exit(app.exec_())
