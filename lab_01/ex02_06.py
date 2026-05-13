# Câu 6: Viết hàm tính giai thừa của một số nguyên dương n.

def giai_thua(n):
    """Tính giai thừa của n (n!)."""
    if n < 0:
        return None
    if n == 0 or n == 1:
        return 1
    ket_qua = 1
    for i in range(2, n + 1):
        ket_qua *= i
    return ket_qua


if __name__ == "__main__":
    n = int(input("Nhập số nguyên dương n: "))
    if n < 0:
        print("Số phải là số nguyên không âm!")
    else:
        print(f"{n}! = {giai_thua(n)}")
