import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from cipher.caesar.caesar_cipher import CaesarCipher
from cipher.vigenere.vigenere_cipher import VigenereCipher
from cipher.rsa.rsa_cipher import RSACipher
from cipher.ecc.ecc_cipher import ECCCipher

app = Flask(__name__)
CORS(app)

caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()
rsa_cipher = RSACipher()
ecc_cipher = ECCCipher()


# --- RSA ENDPOINTS ---

@app.route("/api/rsa/generate_keys", methods=["GET"])
def rsa_generate_keys():
    try:
        msg = rsa_cipher.generate_keys()
        return jsonify({"message": msg})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/rsa/encrypt", methods=["POST"])
def rsa_encrypt():
    data = request.json or {}
    message = data.get("message", "")
    key_type = data.get("key_type", "public")
    
    try:
        private_key, public_key = rsa_cipher.load_keys()
        key = public_key if key_type == "public" else private_key
        encrypted_bytes = rsa_cipher.encrypt(message, key)
        encrypted_hex = encrypted_bytes.hex()
        return jsonify({
            "encrypted_message": encrypted_hex,
            "encrypted_hex": encrypted_hex
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/rsa/decrypt", methods=["POST"])
def rsa_decrypt():
    data = request.json or {}
    ciphertext_hex = data.get("ciphertext", "")
    key_type = data.get("key_type", "private")
    
    try:
        private_key, public_key = rsa_cipher.load_keys()
        key = public_key if key_type == "public" else private_key
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
        decrypted_message = rsa_cipher.decrypt(ciphertext_bytes, key)
        return jsonify({
            "decrypted_message": decrypted_message
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/rsa/sign", methods=["POST"])
def rsa_sign():
    data = request.json or {}
    message = data.get("message", "")
    
    try:
        private_key, _ = rsa_cipher.load_keys()
        signature_bytes = rsa_cipher.sign(message, private_key)
        return jsonify({
            "signature": signature_bytes.hex()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/rsa/verify", methods=["POST"])
def rsa_verify():
    data = request.json or {}
    message = data.get("message", "")
    signature_hex = data.get("signature", "")
    
    try:
        _, public_key = rsa_cipher.load_keys()
        signature_bytes = bytes.fromhex(signature_hex)
        is_verified = rsa_cipher.verify(message, signature_bytes, public_key)
        return jsonify({
            "is_verified": is_verified
        })
    except Exception as e:
        return jsonify({"is_verified": False, "error": str(e)}), 400

# --- ECC ENDPOINTS ---

@app.route("/api/ecc/generate_keys", methods=["GET"])
def ecc_generate_keys():
    try:
        msg = ecc_cipher.generate_keys()
        return jsonify({"message": msg})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ecc/sign", methods=["POST"])
def ecc_sign():
    data = request.json or {}
    message = data.get("message", "")
    
    try:
        private_key, _ = ecc_cipher.load_keys()
        signature_bytes = ecc_cipher.sign(message, private_key)
        return jsonify({
            "signature": signature_bytes.hex()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/ecc/verify", methods=["POST"])
def ecc_verify():
    data = request.json or {}
    message = data.get("message", "")
    signature_hex = data.get("signature", "")
    
    try:
        _, public_key = ecc_cipher.load_keys()
        signature_bytes = bytes.fromhex(signature_hex)
        is_verified = ecc_cipher.verify(message, signature_bytes, public_key)
        return jsonify({
            "is_verified": is_verified
        })
    except Exception as e:
        return jsonify({"is_verified": False, "error": str(e)}), 400

# --- CAESAR & VIGENERE ENDPOINTS (from lab-02) ---

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json or {}
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
    data = request.json or {}
    cipher_text = data.get("cipher_text", "")
    key = data.get("key", 0)
    plain_text = caesar_cipher.decrypt(cipher_text, key)
    return jsonify({
        "cipher_text": cipher_text,
        "key": key,
        "plain_text": plain_text
    })

@app.route("/api/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt_endpoint():
    data = request.json or {}
    plain_text = data.get("plain_text", "")
    key = data.get("key", "")
    cipher_text = vigenere_cipher.encrypt(plain_text, key)
    return jsonify({
        "plain_text": plain_text,
        "key": key,
        "cipher_text": cipher_text
    })

@app.route("/api/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt_endpoint():
    data = request.json or {}
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

