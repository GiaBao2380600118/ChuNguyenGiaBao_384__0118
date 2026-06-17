from cipher.caesar.alphabet import Alphabet

class CaesarCipher:
    def __init__(self):
        self.alphabet = Alphabet()

    def encrypt(self, plain_text, key):
        if not plain_text:
            return ""
        try:
            key = int(key)
        except ValueError:
            return plain_text

        cipher_text = []
        for char in plain_text:
            if char.isupper():
                idx = self.alphabet.get_index(char)
                if idx != -1:
                    new_idx = (idx + key) % 26
                    cipher_text.append(self.alphabet.get_char(new_idx))
                else:
                    cipher_text.append(char)
            elif char.islower():
                idx = self.alphabet.get_index(char)
                if idx != -1:
                    new_idx = (idx + key) % 26
                    cipher_text.append(self.alphabet.get_char(new_idx).lower())
                else:
                    cipher_text.append(char)
            else:
                cipher_text.append(char)
        return "".join(cipher_text)

    def decrypt(self, cipher_text, key):
        if not cipher_text:
            return ""
        try:
            key = int(key)
        except ValueError:
            return cipher_text

        plain_text = []
        for char in cipher_text:
            if char.isupper():
                idx = self.alphabet.get_index(char)
                if idx != -1:
                    new_idx = (idx - key) % 26
                    plain_text.append(self.alphabet.get_char(new_idx))
                else:
                    plain_text.append(char)
            elif char.islower():
                idx = self.alphabet.get_index(char)
                if idx != -1:
                    new_idx = (idx - key) % 26
                    plain_text.append(self.alphabet.get_char(new_idx).lower())
                else:
                    plain_text.append(char)
            else:
                plain_text.append(char)
        return "".join(plain_text)
