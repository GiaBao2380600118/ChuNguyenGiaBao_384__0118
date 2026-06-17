from PIL import Image

def encode_image(img_path, secret_msg, output_path):
    try:
        img = Image.open(img_path)
        img = img.convert('RGB')
        pixels = img.load()
        
        # Add a delimiter to indicate end of message
        secret_msg += "#####"
        binary_msg = ''.join(format(ord(c), '08b') for c in secret_msg)
        
        width, height = img.size
        total_pixels = width * height
        if len(binary_msg) > total_pixels * 3:
            print("[ERROR] Message too large for the image.")
            return False
            
        data_idx = 0
        msg_len = len(binary_msg)
        
        for y in range(height):
            for x in range(width):
                if data_idx < msg_len:
                    r, g, b = pixels[x, y]
                    
                    if data_idx < msg_len:
                        r = (r & ~1) | int(binary_msg[data_idx])
                        data_idx += 1
                    if data_idx < msg_len:
                        g = (g & ~1) | int(binary_msg[data_idx])
                        data_idx += 1
                    if data_idx < msg_len:
                        b = (b & ~1) | int(binary_msg[data_idx])
                        data_idx += 1
                        
                    pixels[x, y] = (r, g, b)
                else:
                    break
            if data_idx >= msg_len:
                break
                
        # Save as PNG format (even with .jpg extension) to prevent lossy compression
        img.save(output_path, format='PNG')
        print(f"[SUCCESS] Message hidden in image and saved to {output_path}")
        return True
    except Exception as e:
        print("[ERROR] Encrypt failed:", e)
        return False

def main():
    secret_msg = input("Enter the secret message to hide: ")
    encode_image("image.jpg", secret_msg, "encoded_image.jpg")

if __name__ == '__main__':
    main()
