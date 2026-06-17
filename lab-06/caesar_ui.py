import tkinter as tk
from tkinter import messagebox, ttk

class CaesarUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Caesar Cipher - Lab 06")
        self.root.geometry("600x500")
        self.root.configure(bg="#121214")
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configure custom styles
        self.style.configure("TLabel", background="#121214", foreground="#E2E2E6", font=("Segoe UI", 11, "bold"))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#9089FC", foreground="#121214", borderwidth=0)
        self.style.map("TButton",
                       background=[("active", "#A59FFA"), ("pressed", "#7B73F0")],
                       foreground=[("active", "#121214")])

        self.create_widgets()

    def create_widgets(self):
        # Title Container
        title_lbl = tk.Label(
            self.root, 
            text="CAESAR CIPHER TOOL", 
            fg="#9089FC", 
            bg="#121214", 
            font=("Segoe UI", 18, "bold"),
            pady=15
        )
        title_lbl.pack()

        # Main Frame
        main_frame = tk.Frame(self.root, bg="#121214", padx=20, pady=10)
        main_frame.pack(fill="both", expand=True)

        # Input text area label
        lbl_plain = tk.Label(main_frame, text="Input Text / Plaintext:", fg="#E2E2E6", bg="#121214", font=("Segoe UI", 10, "bold"))
        lbl_plain.grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Input Text Area
        self.txt_input = tk.Text(
            main_frame, 
            height=6, 
            bg="#1A1A1E", 
            fg="#FFFFFF", 
            insertbackground="#FFFFFF",
            font=("Consolas", 11),
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#2A2A32",
            highlightcolor="#9089FC"
        )
        self.txt_input.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 15))

        # Key selection frame
        key_frame = tk.Frame(main_frame, bg="#121214")
        key_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 15))

        lbl_key = tk.Label(key_frame, text="Shift Key (Integer k):", fg="#E2E2E6", bg="#121214", font=("Segoe UI", 10, "bold"))
        lbl_key.pack(side="left", padx=(0, 10))

        self.ent_key = tk.Entry(
            key_frame,
            width=10,
            bg="#1A1A1E",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            font=("Consolas", 11, "bold"),
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#2A2A32",
            highlightcolor="#9089FC"
        )
        self.ent_key.pack(side="left")
        self.ent_key.insert(0, "3")

        # Action Buttons
        btn_frame = tk.Frame(main_frame, bg="#121214")
        btn_frame.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 15))

        self.btn_encrypt = tk.Button(
            btn_frame,
            text="Mã hóa (Encrypt)",
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
        self.btn_encrypt.pack(side="left", padx=(0, 15))

        self.btn_decrypt = tk.Button(
            btn_frame,
            text="Giải mã (Decrypt)",
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
        self.btn_decrypt.pack(side="left")

        # Output label
        lbl_output = tk.Label(main_frame, text="Result / Ciphertext:", fg="#E2E2E6", bg="#121214", font=("Segoe UI", 10, "bold"))
        lbl_output.grid(row=4, column=0, sticky="w", pady=(0, 5))

        # Output Text Area
        self.txt_output = tk.Text(
            main_frame, 
            height=6, 
            bg="#1A1A1E", 
            fg="#FFFFFF", 
            insertbackground="#FFFFFF",
            font=("Consolas", 11),
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#2A2A32",
            highlightcolor="#9089FC"
        )
        self.txt_output.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=(0, 10))

        # Row/Column configuration to make text areas resize
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(5, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def caesar_cipher(self, text, shift, encrypt=True):
        if not encrypt:
            shift = -shift
        result = []
        for char in text:
            if char.isupper():
                result.append(chr((ord(char) - 65 + shift) % 26 + 65))
            elif char.islower():
                result.append(chr((ord(char) - 97 + shift) % 26 + 97))
            else:
                result.append(char)
        return "".join(result)

    def get_key(self):
        key_str = self.ent_key.get().strip()
        if not key_str:
            messagebox.showerror("Error", "Vui lòng nhập khóa k!")
            return None
        try:
            return int(key_str)
        except ValueError:
            messagebox.showerror("Error", "Khóa k phải là một số nguyên!")
            return None

    def handle_encrypt(self):
        key = self.get_key()
        if key is None:
            return
        
        text = self.txt_input.get("1.0", tk.END).rstrip("\n")
        encrypted = self.caesar_cipher(text, key, encrypt=True)
        
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert("1.0", encrypted)

    def handle_decrypt(self):
        key = self.get_key()
        if key is None:
            return
        
        text = self.txt_input.get("1.0", tk.END).rstrip("\n")
        decrypted = self.caesar_cipher(text, key, encrypt=False)
        
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert("1.0", decrypted)

if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarUI(root)
    root.mainloop()
