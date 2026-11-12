from scatter_plot import parser, COURSES
from itertools import combinations
import sys
import matplotlib.pyplot as plt

# Pair_plot: Permet de voir quel données est différencie vraiment les Maisons, si les nuage sont entremélé les notes dans se domaine ne définisse pas une maison.
# si ils sont séparé c'est le contraire

HOUSES = {"Gryffindor": "red", "Slytherin": "green",
          "Ravenclaw": "blue", "Hufflepuff": "gold"}


def house_pairs(d, a, b, house):
    xs, ys = [], []
    for va, vb, h in zip(d[a], d[b], d["Hogwarts House"]):
        if h == house and va != '' and vb != '':
            xs.append(float(va))
            ys.append(float(vb))
    return xs, ys


def pair_plot(filename):
    d = parser(filename)
    n = len(COURSES)
    fig, axes = plt.subplots(n, n, figsize=(20, 20))

    for a, b in combinations(COURSES, 2):
        i, j = COURSES.index(a), COURSES.index(b)
        for house, color in HOUSES.items():
            xs, ys = house_pairs(d, a, b, house)
            axes[i, j].scatter(ys, xs, s=1, color=color)
            # axes[j, i].scatter(xs, ys, s=1, color=color)

    for i, a in enumerate(COURSES):
        for house, color in HOUSES.items():
            xs, _ = house_pairs(d, a, a, house)
            axes[i, i].hist(xs, bins=20, alpha=0.5, color=color, label=house)

    for i, a in enumerate(COURSES):
        axes[i, 0].set_ylabel(a, fontsize=7, rotation=0, ha='right')
        axes[n - 1, i].set_xlabel(a, fontsize=7, rotation=45, ha='right')
    for ax in axes.flat:
        ax.set_xticks([])
        ax.set_yticks([])

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right')
    plt.subplots_adjust(wspace=0.05, hspace=0.05, left=0.15, bottom=0.12)
    plt.savefig('./../img/pair_plot.png')
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python pair_plot.py <filename>")
        sys.exit(1)
    pair_plot(sys.argv[1])