import math

def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

def md5(message: bytes) -> str:
    # Initial buffer values
    a0 = 0x67452301
    b0 = 0xefcdab89
    c0 = 0x98badcfe
    d0 = 0x10325476

    # MD5 shift table
    s = [
        7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
        5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
        4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
        6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21
    ]

    # MD5 constant table (derived from sine function)
    K = [int(4294967296 * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]

    # Pre-processing: Padding the message
    # Add a single 1 bit (0x80)
    original_len_bits = (len(message) * 8) & 0xffffffffffffffff
    message += b'\x80'

    # Pad with 0s until length in bits is congruent to 448 mod 512
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'

    # Append the original length in bits as a 64-bit little-endian integer
    message += original_len_bits.to_bytes(8, byteorder='little')

    # Process message in 512-bit (64-byte) blocks
    for offset in range(0, len(message), 64):
        block = message[offset:offset+64]
        M = [int.from_bytes(block[i:i+4], byteorder='little') for i in range(0, 64, 4)]
        
        A = a0
        B = b0
        C = c0
        D = d0
        
        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | ((~B) & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | ((~D) & C)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                g = (3 * i + 5) % 16
            elif 48 <= i <= 63:
                F = C ^ (B | (~D))
                g = (7 * i) % 16
                
            F = (F + A + K[i] + M[g]) & 0xFFFFFFFF
            A = D
            D = C
            C = B
            B = (B + left_rotate(F, s[i])) & 0xFFFFFFFF
            
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF

    # Output hash components in little-endian representation
    result = (
        a0.to_bytes(4, byteorder='little') +
        b0.to_bytes(4, byteorder='little') +
        c0.to_bytes(4, byteorder='little') +
        d0.to_bytes(4, byteorder='little')
    )
    return result.hex()

if __name__ == '__main__':
    test_str = "Gia Bao 0118"
    print(f"Hashing string: '{test_str}'")
    print("MD5 Custom Hash:", md5(test_str.encode('utf-8')))
