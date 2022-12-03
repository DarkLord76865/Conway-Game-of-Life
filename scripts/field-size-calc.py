def main():
    for n in range(1, 101):
        for n2 in range(1, 101):
            if ((936 / n) - 1) == ((572 / n2) - 1) and abs(((936 / n) - 1) - round(((936 / n) - 1), 0)) == 0:
                print(n, n2, int(round(((936 / n) - 1), 0)))


if __name__ == '__main__':
    main()
