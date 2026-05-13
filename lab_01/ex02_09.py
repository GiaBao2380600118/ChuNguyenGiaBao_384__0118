# Câu 9: Viết hàm tìm giá trị lớn nhất trong một danh sách số.

def tim_max(danh_sach):
    """Tìm giá trị lớn nhất trong danh sách."""
    if not danh_sach:
        return None
    lon_nhat = danh_sach[0]
    for phan_tu in danh_sach[1:]:
        if phan_tu > lon_nhat:
            lon_nhat = phan_tu
    return lon_nhat


if __name__ == "__main__":
    nhap = input("Nhập các số cách nhau bằng dấu cách: ")
    danh_sach = [float(x) for x in nhap.split()]
    if danh_sach:
        print(f"Giá trị lớn nhất: {tim_max(danh_sach)}")
    else:
        print("Danh sách rỗng!")
