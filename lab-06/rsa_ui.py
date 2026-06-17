import sys
import os
import base64
import tkinter as tk
from tkinter import messagebox, ttk
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class RSAUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Encryption & Decryption - Lab 06 (Even Machine)")
        self.root.geometry("800x700")
        self.root.configure(bg="#121214")

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_lbl = tk.Label(
            self.root,
            text="RSA ENCRYPTION / DECRYPTION",
            fg="#9089FC",
            bg="#121214",
            font=("Segoe UI", 16, "bold"),
            pady=10
        )
        title_lbl.pack()

        # Main Frame
        main_frame = tk.Frame(self.root, bg="#121214", padx=20, pady=10)
        main_frame.pack(fill="both", expand=True)

        # Key Gen Button
        self.btn_gen_keys = tk.Button(
            main_frame,
            text="Generate RSA Key Pair (2048-bit)",
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

        # Key Display Frame
        keys_frame = tk.Frame(main_frame, bg="#121214")
        keys_frame.pack(fill="both", expand=True, pady=(0, 15))
        keys_frame.columnconfigure(0, weight=1)
        keys_frame.columnconfigure(1, weight=1)

        # Private Key
        priv_frame = tk.Frame(keys_frame, bg="#121214")
        priv_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        lbl_priv = tk.Label(priv_frame, text="Private Key (PEM):", fg="#E2E2E6", bg="#121214", font=("Segoe UI", 10, "bold"))
        lbl_priv.pack(anchor="w", pady=(0, 5))
        self.txt_private_key = tk.Text(
            priv_frame,
            height=10,
            bg="#1A1A1E",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            font=("Consolas", 8),
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#2A2A32",
            highlightcolor="#9089FC"
        )
        self.txt_private_key.pack(fill="both", expand=True)

        # Public Key
        pub_frame = tk.Frame(keys_frame, bg="#121214")
        pub_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        lbl_pub = tk.Label(pub_frame, text="Public Key (PEM):", fg="#E2E2E6", bg="#121214", font=("Segoe UI", 10, "bold"))
        lbl_pub.pack(anchor="w", pady=(0, 5))
        self.txt_public_key = tk.Text(
            pub_frame,
            height=10,
            bg="#1A1A1E",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            font=("Consolas", 8),
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
        lbl_cipher = tk.Label(main_frame, text="Cipher Text (Base64 format):", fg="#E2E2E6", bg="#121214", font=("Segoe UI", 10, "bold"))
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

        # Action Buttons
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

    def handle_generate_keys(self):
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            public_key = private_key.public_key()

            # Serialize keys to PEM
            priv_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')

            pub_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')

            self.txt_private_key.delete("1.0", tk.END)
            self.txt_private_key.insert("1.0", priv_pem)
            self.txt_public_key.delete("1.0", tk.END)
            self.txt_public_key.insert("1.0", pub_pem)

            messagebox.showinfo("Success", "RSA Key Pair generated successfully!")
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
            public_key = serialization.load_pem_public_key(pub_pem_str.encode('utf-8'))
            
            # Encrypt with OAEP padding
            ciphertext = public_key.encrypt(
                plaintext.encode('utf-8'),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Encode ciphertext to Base64 for easier transport
            ciphertext_base64 = base64.b64encode(ciphertext).decode('utf-8')
            self.txt_cipher_text.delete("1.0", tk.END)
            self.txt_cipher_text.insert("1.0", ciphertext_base64)
            messagebox.showinfo("Success", "Encrypted Successfully using RSA-OAEP!")
        except Exception as e:
            messagebox.showerror("Encryption Error", f"Failed to encrypt: {str(e)}")

    def handle_decrypt(self):
        priv_pem_str = self.txt_private_key.get("1.0", tk.END).strip()
        ciphertext_base64 = self.txt_cipher_text.get("1.0", tk.END).strip()

        if not priv_pem_str:
            messagebox.showwarning("Input Error", "Please provide a valid Private Key in PEM format.")
            return
        if not ciphertext_base64:
            messagebox.showwarning("Input Error", "Ciphertext cannot be empty.")
            return

        try:
            private_key = serialization.load_pem_private_key(priv_pem_str.encode('utf-8'), password=None)
            ciphertext = base64.b64decode(ciphertext_base64)

            # Decrypt with OAEP padding
            decrypted_bytes = private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            self.txt_plain_text.delete("1.0", tk.END)
            self.txt_plain_text.insert("1.0", decrypted_bytes.decode('utf-8'))
            messagebox.showinfo("Success", "Decrypted Successfully!")
        except Exception as e:
            messagebox.showerror("Decryption Error", f"Failed to decrypt: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RSAUI(root)
    root.mainloop()
