import matplotlib.pyplot as plt
import sys
from describe import std, parser, to_float

# Feature selection :
# Séléction des variable inutile, qui ont un impact homogène sur tout les maisons et donc
# n'apporte pas d'information sur la maison de l'élève. On ne garde que les variables qui ont un impact différent selon la maison.


COURSES = ["Arithmancy", "Astronomy", "Charms",
                "Defense Against the Dark Arts", "Divination", "Herbology",
                "History of Magic", "Potions", "Transfiguration", "Care of Magical Creatures", "Flying"]

def histogram(d, course):
    for maison in ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']:
        notes = [float(v) for v, m in zip(d[course], d['Hogwarts House'])
                 if m == maison and v != '']
        plt.hist(notes, bins=20, alpha=0.5, label=maison)
    plt.suptitle(course, fontsize=9)
    plt.tight_layout()
    plt.savefig('./../img/histogram.png')
    plt.show()


def find_course_homogene(filename):
    d = parser(filename)
    homogeneCourse = None
    for course in COURSES:
        val = std(to_float(d[course]))
        if (not homogeneCourse or val < homogeneCourse["std"]):
            homogeneCourse = {"course": course, "std": val}
    histogram(d, homogeneCourse["course"])
    return homogeneCourse



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python describe.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    find_course_homogene(filename)