import tkinter as tk
from tkinter import messagebox, ttk

class PlayfairUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Playfair Cipher - Lab 06 (Even Machine)")
        self.root.geometry("650x600")
        self.root.configure(bg="#121214")

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_lbl = tk.Label(
            self.root,
            text="PLAYFAIR CIPHER TOOL",
            fg="#9089FC",
            bg="#121214",
            font=("Segoe UI", 18, "bold"),
            pady=15
        )
        title_lbl.pack()

        # Main Frame
        main_frame = tk.Frame(self.root, bg="#121214", padx=20, pady=10)
        main_frame.pack(fill="both", expand=True)

        # Input Text Section
        lbl_plain = tk.Label(main_frame, text="Input Text:", fg="#E2E2E6", bg="#121214", font=("Segoe UI", 10, "bold"))
        lbl_plain.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.txt_input = tk.Text(
            main_frame,
            height=5,
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

        # Key Input Section
        key_frame = tk.Frame(main_frame, bg="#121214")
        key_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 15))

        lbl_key = tk.Label(key_frame, text="Key (String):", fg="#E2E2E6", bg="#121214", font=("Segoe UI", 10, "bold"))
        lbl_key.pack(side="left", padx=(0, 10))

        self.ent_key = tk.Entry(
            key_frame,
            width=25,
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
        self.ent_key.insert(0, "MONARCHY")

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

        # Output Text Section
        lbl_output = tk.Label(main_frame, text="Result:", fg="#E2E2E6", bg="#121214", font=("Segoe UI", 10, "bold"))
        lbl_output.grid(row=4, column=0, sticky="w", pady=(0, 5))

        self.txt_output = tk.Text(
            main_frame,
            height=5,
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
        self.txt_output.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=(0, 15))

        # Matrix View Section (For transparency and better UI experience)
        lbl_matrix = tk.Label(main_frame, text="Key Matrix (5x5):", fg="#E2E2E6", bg="#121214", font=("Segoe UI", 10, "bold"))
        lbl_matrix.grid(row=6, column=0, sticky="w", pady=(0, 5))

        self.lbl_matrix_display = tk.Label(
            main_frame,
            text="",
            fg="#9089FC",
            bg="#1A1A1E",
            font=("Consolas", 12, "bold"),
            bd=1,
            relief="flat",
            padx=15,
            pady=10,
            justify="center"
        )
        self.lbl_matrix_display.grid(row=7, column=0, columnspan=2, sticky="w")

        # Row/Column configuration
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(5, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def generate_matrix(self, key):
        # Format key: uppercase, replace J with I, keep only alphabet letters
        key = key.upper().replace('J', 'I')
        clean_key = []
        for char in key:
            if char.isalpha() and char not in clean_key:
                clean_key.append(char)
        
        # Alphabet without J
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for char in alphabet:
            if char not in clean_key:
                clean_key.append(char)
        
        # Form 5x5 matrix
        matrix = [clean_key[i:i+5] for i in range(0, 25, 5)]
        return matrix

    def find_position(self, matrix, char):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
        return None

    def prepare_text(self, text, encrypt=True):
        # Keep only alphabet, uppercase, J -> I
        text = text.upper().replace('J', 'I')
        clean_text = [char for char in text if char.isalpha()]
        
        if not clean_text:
            return ""

        if not encrypt:
            # Decryption expects even length
            return "".join(clean_text)

        prepared = []
        i = 0
        while i < len(clean_text):
            char1 = clean_text[i]
            if i + 1 < len(clean_text):
                char2 = clean_text[i+1]
                if char1 == char2:
                    prepared.append(char1)
                    prepared.append('X')
                    i += 1
                else:
                    prepared.append(char1)
                    prepared.append(char2)
                    i += 2
            else:
                prepared.append(char1)
                prepared.append('X')
                i += 1
        return "".join(prepared)

    def process_playfair(self, text, key, encrypt=True):
        matrix = self.generate_matrix(key)
        prepared_text = self.prepare_text(text, encrypt=encrypt)
        if not prepared_text:
            return ""

        result = []
        # Update matrix UI
        matrix_str = "\n".join("  ".join(row) for row in matrix)
        self.lbl_matrix_display.config(text=matrix_str)

        # Process in pairs
        for i in range(0, len(prepared_text), 2):
            char1 = prepared_text[i]
            char2 = prepared_text[i+1] if i+1 < len(prepared_text) else 'X'
            
            r1, c1 = self.find_position(matrix, char1)
            r2, c2 = self.find_position(matrix, char2)

            if r1 == r2:
                # Same row: shift right if encrypt, left if decrypt
                shift = 1 if encrypt else -1
                result.append(matrix[r1][(c1 + shift) % 5])
                result.append(matrix[r2][(c2 + shift) % 5])
            elif c1 == c2:
                # Same column: shift down if encrypt, up if decrypt
                shift = 1 if encrypt else -1
                result.append(matrix[(r1 + shift) % 5][c1])
                result.append(matrix[(r2 + shift) % 5][c2])
            else:
                # Rectangle: swap columns
                result.append(matrix[r1][c2])
                result.append(matrix[r2][c1])

        return "".join(result)

    def handle_encrypt(self):
        key = self.ent_key.get().strip()
        if not key:
            messagebox.showerror("Error", "Vui lòng nhập khóa Key!")
            return
        
        text = self.txt_input.get("1.0", tk.END).rstrip("\n")
        if not text:
            messagebox.showerror("Error", "Vui lòng nhập văn bản cần mã hóa!")
            return

        encrypted = self.process_playfair(text, key, encrypt=True)
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert("1.0", encrypted)

    def handle_decrypt(self):
        key = self.ent_key.get().strip()
        if not key:
            messagebox.showerror("Error", "Vui lòng nhập khóa Key!")
            return
        
        text = self.txt_input.get("1.0", tk.END).rstrip("\n")
        if not text:
            messagebox.showerror("Error", "Vui lòng nhập văn bản cần giải mã!")
            return

        decrypted = self.process_playfair(text, key, encrypt=False)
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert("1.0", decrypted)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlayfairUI(root)
    root.mainloop()
