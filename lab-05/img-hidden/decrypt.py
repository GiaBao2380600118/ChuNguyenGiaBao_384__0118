from PIL import Image

def decode_image(img_path):
    try:
        img = Image.open(img_path)
        img = img.convert('RGB')
        pixels = img.load()
        
        binary_data = ""
        width, height = img.size
        
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary_data += str(r & 1)
                binary_data += str(g & 1)
                binary_data += str(b & 1)
                
        # Split binary data into 8-bit characters
        all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
        
        # Convert bytes to characters
        decoded_msg = ""
        for byte in all_bytes:
            if len(byte) < 8:
                break
            char = chr(int(byte, 2))
            decoded_msg += char
            
            # Check for delimiter
            if decoded_msg.endswith("#####"):
                return decoded_msg[:-5]
                
        # If delimiter not found
        return "[WARNING] Delimiter not found. The message might be corrupt or missing."
    except Exception as e:
        return f"[ERROR] Decrypt failed: {e}"

def main():
    img_name = input("Enter image file to decrypt (e.g. encoded_image.jpg or image.jpg): ")
    result = decode_image(img_name)
    print("Decrypted message:", result)

if __name__ == '__main__':
    main()
