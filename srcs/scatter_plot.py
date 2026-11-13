import matplotlib.pyplot as plt
import sys
from describe import std, parser, to_float
from histogram import COURSES
from itertools import combinations


# Coefficient de corrélation de Pearson <pairwise correlations>

def abs(nbr):
    if (nbr < 0):
        return -nbr
    return nbr

def paired(col_a, col_b):
    xs, ys = [], []
    for va, vb in zip(col_a, col_b):
        if va is not None and vb is not None:
            xs.append(va)
            ys.append(vb)
    return xs, ys

def coefPearson(ax, ay):
    if (len(ax) != len(ay)): return 0
    meanx, meany = sum(ax) / len(ax), sum(ay) / len(ay)
    part1 = sum(((x - meanx) * (y - meany)) for x, y in zip(ax, ay))
    part2 = (
                    sum(((x - meanx) ** 2) for x in ax) *
                    sum(((y - meany) ** 2) for y in ay)
            ) ** 0.5
    return part1 / part2

def scatter_plot_display(d, correlation):
    a, b = correlation["pair1"], correlation["pair2"]
    xs, ys = paired(d[a], d[b])
    plt.scatter(xs, ys, s=4)
    plt.xlabel(a)
    plt.ylabel(b)
    plt.title(f"r = {correlation['coef']:.3f}")
    plt.savefig('./../img/scatter_plot.png')
    plt.show()

def scatter_plot(filename):
    d = parser(filename)
    correlations = None
    for a, b in combinations(COURSES, 2):
        xs, ys = paired(d[a], d[b])
        coef = coefPearson(xs, ys)
        if not correlations or abs(coef) > abs(correlations["coef"]):
            correlations = {"coef": coef, "pair1": a, "pair2": b}
    scatter_plot_display(d, correlations)
    return correlations



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python describe.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    scatter_plot(filename)