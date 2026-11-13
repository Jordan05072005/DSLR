import matplotlib.pyplot as plt
import sys
from describe import std, parser, to_float

# Feature selection :
# Séléction des variable inutile, qui ont un impact homogène sur tout les maisons et donc
# n'apporte pas d'information sur la maison de l'élève. On ne garde que les variables qui ont un impact différent selon la maison.


COURSES = ["Arithmancy", "Astronomy", "Charms",
                "Defense Against the Dark Arts", "Divination", "Herbology",
                "History of Magic", "Potions", "Transfiguration", "Care of Magical Creatures", "Flying"]

HOUSES = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]


def histogram(d, course):
    for house in ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']:
        notes = [v for v, m in zip(d[course], d['Hogwarts House'])
                 if m == house and v is not None]
        plt.hist(notes, bins=20, alpha=0.5, label=house )
    plt.suptitle(course, fontsize=9)
    plt.tight_layout()
    plt.savefig('./../img/histogram.png')
    # plt.show()

def fisherScore(d, course):
    notes = [v for v in d[course] if v is not None]
    meanAll = sum(notes) / len(notes)

    num, den = 0.0, 0.0
    for house in HOUSES:
        notes_house = [v for v, h in zip(d[course], d["Hogwarts House"])
                       if h == house and v is not None]
        n_c = len(notes_house)
        meanHouse = sum(notes_house) / n_c
        stdHouse = std(notes_house)
        num += n_c * (meanHouse - meanAll) ** 2
        den += n_c * stdHouse ** 2
    return num / den


def find_course_homogene(filename):
    d = parser(filename)
    homogeneCourse = None
    for course in COURSES:
        val = fisherScore(d, course)
        if (not homogeneCourse or val < homogeneCourse["fisherScore"]):
            homogeneCourse = {"course": course, "fisherScore": val}
    histogram(d, homogeneCourse["course"])
    return homogeneCourse



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python describe.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    find_course_homogene(filename)