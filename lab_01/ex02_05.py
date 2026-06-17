# Câu 5: Viết chương trình kiểm tra một số nguyên là chẵn hay lẻ.

def kiem_tra_chan_le(n):
    """Kiểm tra số n là chẵn hay lẻ."""
    if n % 2 == 0:
        return "chẵn"
    else:
        return "lẻ"


if __name__ == "__main__":
    n = int(input("Nhập một số nguyên: "))
    print(f"Số {n} là số {kiem_tra_chan_le(n)}.")
