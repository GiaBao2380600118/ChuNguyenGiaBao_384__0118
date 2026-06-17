class VigenereCipher:
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def encrypt(self, plain_text, key):
        if not plain_text or not key:
            return ""
        key = key.upper()
        cipher_text = []
        key_index = 0
        for char in plain_text:
            if char.isalpha():
                shift = self.alphabet.find(key[key_index % len(key)])
                if char.isupper():
                    idx = self.alphabet.find(char)
                    new_idx = (idx + shift) % 26
                    cipher_text.append(self.alphabet[new_idx])
                else:
                    idx = self.alphabet.find(char.upper())
                    new_idx = (idx + shift) % 26
                    cipher_text.append(self.alphabet[new_idx].lower())
                key_index += 1
            else:
                cipher_text.append(char)
        return "".join(cipher_text)

    def decrypt(self, cipher_text, key):
        if not cipher_text or not key:
            return ""
        key = key.upper()
        plain_text = []
        key_index = 0
        for char in cipher_text:
            if char.isalpha():
                shift = self.alphabet.find(key[key_index % len(key)])
                if char.isupper():
                    idx = self.alphabet.find(char)
                    new_idx = (idx - shift) % 26
                    plain_text.append(self.alphabet[new_idx])
                else:
                    idx = self.alphabet.find(char.upper())
                    new_idx = (idx - shift) % 26
                    plain_text.append(self.alphabet[new_idx].lower())
                key_index += 1
            else:
                plain_text.append(char)
        return "".join(plain_text)
