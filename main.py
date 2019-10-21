import des

def main():
    key = input()
    msg = input()
    count = int(input())

    for _ in range(count):
        msg = des.encrypt(msg, key)

    print(msg)

if __name__ == "__main__":
    main()
