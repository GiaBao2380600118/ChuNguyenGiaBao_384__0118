# Câu 7: Viết hàm kiểm tra một số có phải là số nguyên tố hay không.

def la_so_nguyen_to(n):
    """Kiểm tra n có phải là số nguyên tố không."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    n = int(input("Nhập một số nguyên: "))
    if la_so_nguyen_to(n):
        print(f"{n} là số nguyên tố.")
    else:
        print(f"{n} không phải là số nguyên tố.")
