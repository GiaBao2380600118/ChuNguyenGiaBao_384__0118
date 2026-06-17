# Câu 4: Viết chương trình đổi nhiệt độ từ độ Celsius sang độ Fahrenheit.
# Công thức: F = C * 9/5 + 32

def celsius_to_fahrenheit(celsius):
    """Chuyển đổi nhiệt độ từ Celsius sang Fahrenheit."""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """Chuyển đổi nhiệt độ từ Fahrenheit sang Celsius."""
    return (fahrenheit - 32) * 5 / 9


if __name__ == "__main__":
    c = float(input("Nhập nhiệt độ (°C): "))
    f = celsius_to_fahrenheit(c)
    print(f"{c}°C = {f:.2f}°F")
