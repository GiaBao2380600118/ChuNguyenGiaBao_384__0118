# Câu 10: Viết một hàm nhận vào một chuỗi và trả về chuỗi đảo ngược của nó.

def reverse_string(s):
    """Nhận vào một chuỗi và trả về chuỗi đảo ngược."""
    return s[::-1]


# Test thử hàm
if __name__ == "__main__":
    chuoi = input("Nhập chuỗi: ")
    ket_qua = reverse_string(chuoi)
    print(f"Chuỗi đảo ngược: {ket_qua}")
