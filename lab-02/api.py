from flask import Flask, request, jsonify
from flask_cors import CORS
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request body"}), 400
    plain_text = data.get("plain_text", "")
    key = data.get("key", 0)
    
    cipher_text = caesar_cipher.encrypt(plain_text, key)
    return jsonify({
        "plain_text": plain_text,
        "key": key,
        "cipher_text": cipher_text
    })

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request body"}), 400
    cipher_text = data.get("cipher_text", "")
    key = data.get("key", 0)
    
    plain_text = caesar_cipher.decrypt(cipher_text, key)
    return jsonify({
        "cipher_text": cipher_text,
        "key": key,
        "plain_text": plain_text
    })

@app.route("/api/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request body"}), 400
    plain_text = data.get("plain_text", "")
    key = data.get("key", "")
    
    cipher_text = vigenere_cipher.encrypt(plain_text, key)
    return jsonify({
        "plain_text": plain_text,
        "key": key,
        "cipher_text": cipher_text
    })

@app.route("/api/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request body"}), 400
    cipher_text = data.get("cipher_text", "")
    key = data.get("key", "")
    
    plain_text = vigenere_cipher.decrypt(cipher_text, key)
    return jsonify({
        "cipher_text": cipher_text,
        "key": key,
        "plain_text": plain_text
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
