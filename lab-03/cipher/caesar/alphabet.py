class Alphabet:
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def get_index(self, char):
        return self.alphabet.find(char.upper())

    def get_char(self, index):
        return self.alphabet[index % len(self.alphabet)]
