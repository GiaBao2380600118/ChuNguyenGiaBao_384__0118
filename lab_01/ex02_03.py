# Câu 3: Viết chương trình tính diện tích và chu vi hình chữ nhật.

def tinh_dien_tich(dai, rong):
    """Tính diện tích hình chữ nhật."""
    return dai * rong


def tinh_chu_vi(dai, rong):
    """Tính chu vi hình chữ nhật."""
    return 2 * (dai + rong)


if __name__ == "__main__":
    dai = float(input("Nhập chiều dài: "))
    rong = float(input("Nhập chiều rộng: "))
    print(f"Diện tích: {tinh_dien_tich(dai, rong)}")
    print(f"Chu vi: {tinh_chu_vi(dai, rong)}")
