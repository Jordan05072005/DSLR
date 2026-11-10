import matplotlib.pyplot as plt
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

def histogram(filename):
    d = parser(filename)
    matieres = ["Arithmancy", "Astronomy", "Charms",
                "Defense Against the Dark Arts", "Divination", "Herbology",
                "History of Magic", "Potions", "Transfiguration", "Care of Magical Creatures", "Charms", "Flying"]

    user = list(range(len(d["Astronomy"])))
    cols = 4
    rows = (len(matieres) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3 * rows))
    axes = axes.flatten()
    for i, cours in enumerate(matieres):
        for maison in ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']:
            notes = [float(v) for v, m in zip(d[cours], d['Hogwarts House'])
                     if m == maison and v != '']
            axes[i].hist(notes, bins=20, alpha=0.5, label=maison)
            axes[i].set_title(cours, fontsize=9)
    plt.tight_layout()
    plt.savefig('histogram.png')
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python describe.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    histogram(filename)