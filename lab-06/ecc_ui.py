import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

class ECCUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ECC Encryption & Decryption - Lab 06")
        self.root.geometry("800x700")
        self.root.configure(bg="#121214")
        
        self.create_widgets()
        self.load_keys_from_disk()

    def create_widgets(self):
        # Title Label
        title_lbl = tk.Label(
            self.root,
            text="ECC ENCRYPTION / DECRYPTION",
            fg="#9089FC",
            bg="#121214",
            font=("Segoe UI", 16, "bold"),
            pady=10
        )
        title_lbl.pack()

        # Main Scrollable or Pack Container
        main_frame = tk.Frame(self.root, bg="#121214", padx=20, pady=10)
        main_frame.pack(fill="both", expand=True)

        # Key Gen Button
        self.btn_gen_keys = tk.Button(
            main_frame,
            text="Generate ECC Key Pair (secp256r1)",
            command=self.handle_generate_keys,
            bg="#9089FC",
            fg="#121214",
            activebackground="#A59FFA",
            activeforeground="#121214",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            pady=8,
            cursor="hand2"
        )
        self.btn_gen_keys.pack(fill="x", pady=(0, 15))

        # Key Display Frame (Horizontal Layout)
        keys_frame = tk.Frame(main_frame, bg="#121214")
        keys_frame.pack(fill="both", expand=True, pady=(0, 15))
        keys_frame.columnconfigure(0, weight=1)
        keys_frame.columnconfigure(1, weight=1)

        # Private Key Display
        priv_frame = tk.Frame(keys_frame, bg="#121214")
        priv_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        lbl_priv = tk.Label(priv_frame, text="Private Key (PEM):", fg="#E2E2E6", bg="#121214", font=("Segoe UI", 10, "bold"))
        lbl_priv.pack(anchor="w", pady=(0, 5))
        self.txt_private_key = tk.Text(
            priv_frame,
            height=8,
            bg="#1A1A1E",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            font=("Consolas", 9),
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#2A2A32",
            highlightcolor="#9089FC"
        )
        self.txt_private_key.pack(fill="both", expand=True)

        # Public Key Display
        pub_frame = tk.Frame(keys_frame, bg="#121214")
        pub_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        lbl_pub = tk.Label(pub_frame, text="Public Key (PEM):", fg="#E2E2E6", bg="#121214", font=("Segoe UI", 10, "bold"))
        lbl_pub.pack(anchor="w", pady=(0, 5))
        self.txt_public_key = tk.Text(
            pub_frame,
            height=8,
            bg="#1A1A1E",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            font=("Consolas", 9),
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#2A2A32",
            highlightcolor="#9089FC"
        )
        self.txt_public_key.pack(fill="both", expand=True)

        # Plaintext Section
        lbl_plain = tk.Label(main_frame, text="Plain Text:", fg="#E2E2E6", bg="#121214", font=("Segoe UI", 10, "bold"))
        lbl_plain.pack(anchor="w", pady=(0, 5))
        self.txt_plain_text = tk.Text(
            main_frame,
            height=4,
            bg="#1A1A1E",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            font=("Consolas", 10),
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#2A2A32",
            highlightcolor="#9089FC"
        )
        self.txt_plain_text.pack(fill="both", expand=True, pady=(0, 15))

        # Ciphertext Section
        lbl_cipher = tk.Label(main_frame, text="Cipher Text (Format: ephemeral_key:iv:tag:ciphertext in hex):", fg="#E2E2E6", bg="#121214", font=("Segoe UI", 10, "bold"))
        lbl_cipher.pack(anchor="w", pady=(0, 5))
        self.txt_cipher_text = tk.Text(
            main_frame,
            height=4,
            bg="#1A1A1E",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            font=("Consolas", 10),
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#2A2A32",
            highlightcolor="#9089FC"
        )
        self.txt_cipher_text.pack(fill="both", expand=True, pady=(0, 15))

        # Bottom Action Buttons
        btn_action_frame = tk.Frame(main_frame, bg="#121214")
        btn_action_frame.pack(fill="x")

        self.btn_encrypt = tk.Button(
            btn_action_frame,
            text="Encrypt with Public Key",
            command=self.handle_encrypt,
            bg="#9089FC",
            fg="#121214",
            activebackground="#A59FFA",
            activeforeground="#121214",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.btn_encrypt.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_decrypt = tk.Button(
            btn_action_frame,
            text="Decrypt with Private Key",
            command=self.handle_decrypt,
            bg="#9089FC",
            fg="#121214",
            activebackground="#A59FFA",
            activeforeground="#121214",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.btn_decrypt.pack(side="right", fill="x", expand=True, padx=(10, 0))

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
                self.txt_private_key.delete("1.0", tk.END)
                self.txt_private_key.insert("1.0", priv_pem)
                self.txt_public_key.delete("1.0", tk.END)
                self.txt_public_key.insert("1.0", pub_pem)
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

            self.txt_private_key.delete("1.0", tk.END)
            self.txt_private_key.insert("1.0", priv_pem)
            self.txt_public_key.delete("1.0", tk.END)
            self.txt_public_key.insert("1.0", pub_pem)
            messagebox.showinfo("Success", "ECC Key Pair generated successfully and saved to disk!")
        except Exception as e:
            messagebox.showerror("Key Gen Error", f"Failed to generate keys: {str(e)}")

    def handle_encrypt(self):
        pub_pem_str = self.txt_public_key.get("1.0", tk.END).strip()
        plaintext = self.txt_plain_text.get("1.0", tk.END).rstrip("\n")
        
        if not pub_pem_str:
            messagebox.showwarning("Input Error", "Please provide a valid Public Key in PEM format.")
            return
        if not plaintext:
            messagebox.showwarning("Input Error", "Plaintext cannot be empty.")
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
            self.txt_cipher_text.delete("1.0", tk.END)
            self.txt_cipher_text.insert("1.0", formatted_ciphertext)
            messagebox.showinfo("Success", "Encrypted Successfully using ECIES!")
        except Exception as e:
            messagebox.showerror("Encryption Error", f"Failed to encrypt: {str(e)}")

    def handle_decrypt(self):
        priv_pem_str = self.txt_private_key.get("1.0", tk.END).strip()
        ciphertext_str = self.txt_cipher_text.get("1.0", tk.END).strip()
        
        if not priv_pem_str:
            messagebox.showwarning("Input Error", "Please provide a valid Private Key in PEM format.")
            return
        if not ciphertext_str:
            messagebox.showwarning("Input Error", "Ciphertext cannot be empty.")
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

            self.txt_plain_text.delete("1.0", tk.END)
            self.txt_plain_text.insert("1.0", decrypted_bytes.decode('utf-8'))
            messagebox.showinfo("Success", "Decrypted Successfully using ECIES!")
        except Exception as e:
            messagebox.showerror("Decryption Error", f"Failed to decrypt: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ECCUI(root)
    root.mainloop()
