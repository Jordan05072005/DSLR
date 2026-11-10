import sys

def parser(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        keys = f.readline().rstrip().split(',')
        d = {key: [] for key in keys}
        for line in f:
            values = line.rstrip().split(',')
            for key, value in zip(keys, values):
                d[key].append(value)
    print(d)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python describe.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    parser(filename)
