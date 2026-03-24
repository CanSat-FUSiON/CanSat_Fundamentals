def read_float(label: str) -> float:
    while True:
        try:
            return float(input(f"{label}? "))
        except ValueError:
            print("数値を入力してください")

def main() -> None:
    a = read_float("a")
    while True:
        try:
            b = read_float("b")
            print("結果:", a / b)
            break
        except ZeroDivisionError:
            print("0では割れません")

if __name__ == "__main__":
    main()
