import sys
import os

# Set QT_QPA_PLATFORM_PLUGIN_PATH
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.path.dirname(__file__), 'platforms')

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ciphers_q1 import Ui_MainWindow

# --- CRYPTOGRAPHIC ALGORITHMS ---

# 1. Vigenere
def vigenere_encrypt(text, key):
    key = key.upper()
    if not key:
        return text
    cipher = []
    key_idx = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            c = chr((ord(char) - base + shift) % 26 + base)
            cipher.append(c)
            key_idx += 1
        else:
            cipher.append(char)
    return "".join(cipher)

def vigenere_decrypt(cipher, key):
    key = key.upper()
    if not key:
        return cipher
    plain = []
    key_idx = 0
    for char in cipher:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            p = chr((ord(char) - base - shift) % 26 + base)
            plain.append(p)
            key_idx += 1
        else:
            plain.append(char)
    return "".join(plain)

# 2. Rail Fence
def rail_fence_encrypt(text, key):
    try:
        key = int(key)
    except ValueError:
        return text
    if key <= 1:
        return text
    
    grid = [['\n' for _ in range(len(text))] for _ in range(key)]
    row, col = 0, 0
    direction_down = False
    
    for char in text:
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        
        grid[row][col] = char
        col += 1
        
        if direction_down:
            row += 1
        else:
            row -= 1
            
    result = []
    for r in range(key):
        for c in range(len(text)):
            if grid[r][c] != '\n':
                result.append(grid[r][c])
    return "".join(result)

def rail_fence_decrypt(cipher, key):
    try:
        key = int(key)
    except ValueError:
        return cipher
    if key <= 1:
        return cipher
        
    grid = [['\n' for _ in range(len(cipher))] for _ in range(key)]
    row, col = 0, 0
    direction_down = None
    
    for i in range(len(cipher)):
        if row == 0:
            direction_down = True
        if row == key - 1:
            direction_down = False
            
        grid[row][col] = '*'
        col += 1
        
        if direction_down:
            row += 1
        else:
            row -= 1
            
    index = 0
    for r in range(key):
        for c in range(len(cipher)):
            if grid[r][c] == '*' and index < len(cipher):
                grid[r][c] = cipher[index]
                index += 1
                
    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            direction_down = True
        if row == key - 1:
            direction_down = False
            
        if grid[row][col] != '\n':
            result.append(grid[row][col])
            col += 1
            
        if direction_down:
            row += 1
        else:
            row -= 1
    return "".join(result)

# 3. Playfair
def playfair_prepare_key(key):
    key = key.upper().replace('J', 'I')
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key_string = ""
    for char in key:
        if char.isalpha() and char not in key_string:
            key_string += char
    for char in alphabet:
        if char not in key_string:
            key_string += char
    return key_string

def playfair_encrypt(text, key):
    key_string = playfair_prepare_key(key)
    text = "".join([c.upper() for c in text if c.isalpha()]).replace('J', 'I')
    if not text:
        return ""
    prepared_text = ""
    i = 0
    while i < len(text):
        c1 = text[i]
        c2 = text[i+1] if (i+1) < len(text) else 'X'
        if c1 == c2:
            prepared_text += c1 + 'X'
            i += 1
        else:
            prepared_text += c1 + c2
            i += 2
    if len(prepared_text) % 2 != 0:
        prepared_text += 'X'
        
    cipher = ""
    for i in range(0, len(prepared_text), 2):
        c1, c2 = prepared_text[i], prepared_text[i+1]
        row1, col1 = key_string.index(c1) // 5, key_string.index(c1) % 5
        row2, col2 = key_string.index(c2) // 5, key_string.index(c2) % 5
        
        if row1 == row2:
            col1 = (col1 + 1) % 5
            col2 = (col2 + 1) % 5
        elif col1 == col2:
            row1 = (row1 + 1) % 5
            row2 = (row2 + 1) % 5
        else:
            col1, col2 = col2, col1
            
        cipher += key_string[row1 * 5 + col1] + key_string[row2 * 5 + col2]
    return cipher

def playfair_decrypt(cipher, key):
    key_string = playfair_prepare_key(key)
    cipher = "".join([c.upper() for c in cipher if c.isalpha()]).replace('J', 'I')
    if not cipher:
        return ""
    plain = ""
    for i in range(0, len(cipher), 2):
        c1, c2 = cipher[i], cipher[i+1]
        row1, col1 = key_string.index(c1) // 5, key_string.index(c1) % 5
        row2, col2 = key_string.index(c2) // 5, key_string.index(c2) % 5
        
        if row1 == row2:
            col1 = (col1 - 1) % 5
            col2 = (col2 - 1) % 5
        elif col1 == col2:
            row1 = (row1 - 1) % 5
            row2 = (row2 - 1) % 5
        else:
            col1, col2 = col2, col1
            
        plain += key_string[row1 * 5 + col1] + key_string[row2 * 5 + col2]
    return plain

# 4. Transposition
def transposition_encrypt(text, key):
    if not key:
        return text
    num_cols = len(key)
    num_rows = (len(text) + num_cols - 1) // num_cols
    padded_text = text.ljust(num_rows * num_cols, 'X')
    grid = [padded_text[i:i+num_cols] for i in range(0, len(padded_text), num_cols)]
    
    # Sort columns by key alphabetically
    key_indices = sorted(range(len(key)), key=lambda k: key[k])
    
    cipher = ""
    for col in key_indices:
        for row in range(num_rows):
            cipher += grid[row][col]
    return cipher

def transposition_decrypt(cipher, key):
    if not key:
        return cipher
    num_cols = len(key)
    num_rows = len(cipher) // num_cols
    grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    
    key_indices = sorted(range(len(key)), key=lambda k: key[k])
    
    index = 0
    for col in key_indices:
        for row in range(num_rows):
            if index < len(cipher):
                grid[row][col] = cipher[index]
                index += 1
                
    plain = ""
    for row in range(num_rows):
        plain += "".join(grid[row])
    return plain.rstrip('X')


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect Vigenere
        self.ui.btn_v_encrypt.clicked.connect(self.vig_encrypt_slot)
        self.ui.btn_v_decrypt.clicked.connect(self.vig_decrypt_slot)
        
        # Connect Rail Fence
        self.ui.btn_rf_encrypt.clicked.connect(self.rf_encrypt_slot)
        self.ui.btn_rf_decrypt.clicked.connect(self.rf_decrypt_slot)
        
        # Connect Playfair
        self.ui.btn_pf_encrypt.clicked.connect(self.pf_encrypt_slot)
        self.ui.btn_pf_decrypt.clicked.connect(self.pf_decrypt_slot)
        
        # Connect Transposition
        self.ui.btn_tr_encrypt.clicked.connect(self.tr_encrypt_slot)
        self.ui.btn_tr_decrypt.clicked.connect(self.tr_decrypt_slot)
        
        # Apply premium styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121214;
            }
            QLabel {
                color: #E2E2E6;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }
            QLabel#label_title {
                color: #9089FC;
                font-size: 20px;
                font-weight: bold;
                margin: 10px;
            }
            QPlainTextEdit, QLineEdit {
                background-color: #1A1A1E;
                color: #FFFFFF;
                border: 1px solid #2A2A32;
                border-radius: 6px;
                padding: 6px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
            }
            QPlainTextEdit:focus, QLineEdit:focus {
                border: 1px solid #9089FC;
            }
            QPushButton {
                background-color: #9089FC;
                color: #121214;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #A59FFA;
            }
            QPushButton:pressed {
                background-color: #7B73F0;
            }
            QTabWidget::pane {
                border: 1px solid #2A2A32;
                background: #121214;
                border-radius: 6px;
            }
            QTabBar::tab {
                background: #1A1A1E;
                color: #A0A0AA;
                border: 1px solid #2A2A32;
                padding: 8px 12px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: #121214;
                color: #FFFFFF;
                border-bottom-color: #121214;
            }
            QTabBar::tab:selected {
                border-color: #9089FC;
                border-bottom-color: #121214;
                font-weight: bold;
            }
        """)

    # Vigenere slots
    def vig_encrypt_slot(self):
        text = self.ui.txt_v_plain.toPlainText()
        key = self.ui.txt_v_key.text()
        if not key:
            QMessageBox.warning(self, "Input Error", "Please provide a key!")
            return
        result = vigenere_encrypt(text, key)
        self.ui.txt_v_cipher.setPlainText(result)
        
    def vig_decrypt_slot(self):
        cipher = self.ui.txt_v_cipher.toPlainText()
        key = self.ui.txt_v_key.text()
        if not key:
            QMessageBox.warning(self, "Input Error", "Please provide a key!")
            return
        result = vigenere_decrypt(cipher, key)
        self.ui.txt_v_plain.setPlainText(result)

    # Rail Fence slots
    def rf_encrypt_slot(self):
        text = self.ui.txt_rf_plain.toPlainText()
        key = self.ui.txt_rf_key.text()
        if not key:
            QMessageBox.warning(self, "Input Error", "Please provide a numeric key (rails)!")
            return
        result = rail_fence_encrypt(text, key)
        self.ui.txt_rf_cipher.setPlainText(result)
        
    def rf_decrypt_slot(self):
        cipher = self.ui.txt_rf_cipher.toPlainText()
        key = self.ui.txt_rf_key.text()
        if not key:
            QMessageBox.warning(self, "Input Error", "Please provide a numeric key (rails)!")
            return
        result = rail_fence_decrypt(cipher, key)
        self.ui.txt_rf_plain.setPlainText(result)

    # Playfair slots
    def pf_encrypt_slot(self):
        text = self.ui.txt_pf_plain.toPlainText()
        key = self.ui.txt_pf_key.text()
        if not key:
            QMessageBox.warning(self, "Input Error", "Please provide a key string!")
            return
        result = playfair_encrypt(text, key)
        self.ui.txt_pf_cipher.setPlainText(result)
        
    def pf_decrypt_slot(self):
        cipher = self.ui.txt_pf_cipher.toPlainText()
        key = self.ui.txt_pf_key.text()
        if not key:
            QMessageBox.warning(self, "Input Error", "Please provide a key string!")
            return
        result = playfair_decrypt(cipher, key)
        self.ui.txt_pf_plain.setPlainText(result)

    # Transposition slots
    def tr_encrypt_slot(self):
        text = self.ui.txt_tr_plain.toPlainText()
        key = self.ui.txt_tr_key.text()
        if not key:
            QMessageBox.warning(self, "Input Error", "Please provide a key keyword!")
            return
        result = transposition_encrypt(text, key)
        self.ui.txt_tr_cipher.setPlainText(result)
        
    def tr_decrypt_slot(self):
        cipher = self.ui.txt_tr_cipher.toPlainText()
        key = self.ui.txt_tr_key.text()
        if not key:
            QMessageBox.warning(self, "Input Error", "Please provide a key keyword!")
            return
        result = transposition_decrypt(cipher, key)
        self.ui.txt_tr_plain.setPlainText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
