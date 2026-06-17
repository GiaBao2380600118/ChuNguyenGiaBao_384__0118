# Câu 2: Viết chương trình nhập vào hai số nguyên và in ra tổng của chúng.

def tinh_tong(a, b):
    """Tính tổng hai số nguyên."""
    return a + b


if __name__ == "__main__":
    a = int(input("Nhập số thứ nhất: "))
    b = int(input("Nhập số thứ hai: "))
    print(f"Tổng của {a} và {b} là: {tinh_tong(a, b)}")
