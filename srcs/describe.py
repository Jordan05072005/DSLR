import sys

def parser(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        keys = f.readline().rstrip().split(',')
        d = {key: [] for key in keys}
        for line in f:
            values = line.rstrip().split(',')
            for key, value in zip(keys, values):
                d[key].append(value)
    return d


def std(arr):
    n = len(arr)
    mean = sum(arr) / n
    total = 0
    for x in arr:
        total += (x - mean) ** 2
    return (total / (n - 1)) ** 0.5


def percentile(arr, p):
    s = sorted(arr)
    n = len(s)
    rang = (p / 100) * (n - 1)
    bas = int(rang)
    reste = rang - bas
    if bas + 1 < n:
        return s[bas] + reste * (s[bas + 1] - s[bas])
    return s[bas]


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def to_float(values):
    return [float(v) for v in values if v != '' and is_number(v)]

def describe(d):
    fun=[
         {"name": "Count", "func": lambda arr: len(arr)},
         {"name": "Mean", "func": lambda arr: sum(arr) / len(arr)},
         {"name": "Std", "func": std },
         {"name": "Min", "func": lambda arr: min(arr)},
         {"name": "25", "func": lambda arr: percentile(arr, 25)},
        {"name": "50", "func": lambda arr: percentile(arr, 50)},
        {"name": "75", "func": lambda arr: percentile(arr, 75)},
        {"name": "Max", "func": lambda arr: max(arr)}
    ]
    numeric = {}
    for key, values in d.items():
        floats = to_float(values)
        if len(floats) > 0 and len(floats) == len([v for v in values if v != '']):
            numeric[key] = floats

    header = "".join(f"{key[:13]:>15}" for key in numeric)
    print(f"{'':>6}{header}")

    for stat in fun:
        row = "".join(f"{stat['func'](numeric[key]):>15.6f}" for key in numeric)
        print(f"{stat['name']:>6}{row}")



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python describe.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    describe(parser(filename))
