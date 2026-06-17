# Câu 8: Viết chương trình in bảng cửu chương của một số từ 1 đến 10.

def in_bang_cuu_chuong(n):
    """In bảng cửu chương của số n."""
    print(f"--- Bảng cửu chương {n} ---")
    for i in range(1, 11):
        print(f"{n} x {i:2d} = {n * i:3d}")


if __name__ == "__main__":
    n = int(input("Nhập số cần in bảng cửu chương (1-9): "))
    if 1 <= n <= 9:
        in_bang_cuu_chuong(n)
    else:
        print("Vui lòng nhập số từ 1 đến 9!")
