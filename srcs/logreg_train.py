from describe import std, parser
from histogram import COURSES, to_float, fisherScore
from scatter_plot import paired, coefPearson
import sys, math
from itertools import combinations
import random


THRESHOLD_FISHER = 0.1
THRESHOLD_COEF_PEARSON = 0.95

def paser_to_unuseful_stuff(d):
    coursesUse = list(COURSES)
    for course in COURSES:
        val = fisherScore(d, course)
        if (val < THRESHOLD_FISHER):
            coursesUse.remove(course)
    for a, b in combinations(COURSES, 2):
        if not ((a in coursesUse) and (b in coursesUse)): continue
        xs, ys = paired(d[a], d[b])
        coef = coefPearson(xs, ys)
        if abs(coef) > THRESHOLD_COEF_PEARSON:
            coursesUse.remove(a) #or b
    return coursesUse

def sigma(z): # normalise ou on limite
    z = max(-500, min(500, z))
    return 1 / (1 + math.exp(-z))

def prediction(data, bias, weights, coursesUse):
    sum = bias
    for i, value in enumerate(data):
        sum += (value * weights[coursesUse[i]])
    return sigma(sum)


def write(bias, weights, stats):
    with open('./../ressources/weights.txt', 'w') as f:
        for house, weight in weights.items():
            f.write(f"{house}_bias={bias[house]}\n")
            for course, value in weight.items():
                f.write(f"{house}_{course}_weight={value}\n")
        for (course, value) in stats.items():
            f.write(f"{course}_mean={value[0]}\n")
            f.write(f"{course}_std={value[1]}\n")

def normalisation(arr, min, max, sur): # norm a une note plus base, moins performant
    for i in range(len(arr)):
        arr[i] = (arr[i] - min) / (max - min) * sur
    return arr

def standardization(arr, mean_init=None, std_value_init=None):  # centre les notes sur 0, en unités d'écart-type
    mean = mean_init or sum(arr) / len(arr)
    std_value = std_value_init or std(arr)
    for i in range(len(arr)):
        arr[i] = (arr[i] - mean ) / std_value
    return arr, mean, std_value


def GradientDescent(d, bias, weights, pas, courseUse, house):
    errors = []
    cout  = 0
    errorsNotes = {course: 0 for course in courseUse}
    for ligne in range(len(d["First Name"])):
        data = [d[course][ligne] for course in courseUse]
        prediction_value = prediction(data, bias, weights,courseUse)
        correct = (d["Hogwarts House"][ligne] == house)
        error = prediction_value - correct
        h = min(max(prediction_value, 1e-15), 1 - 1e-15)
        cout += correct * math.log(h) + (1 - correct) * math.log(1 - h)
        for i, course in enumerate(courseUse):
            errorsNotes[course] += (error * data[i])
        errors.append(error)
    for course in courseUse:
        meanErrorNote = errorsNotes[course] / len(errors)
        weights[course] = weights[course] - pas * (meanErrorNote)
    meanError = sum(errors) / len(errors)
    print("House: ", house," Cout: ", -cout / len(errors))
    return bias - pas * (meanError)

# est plus rapide car il met a jours la poid et le biais pour chaque user, permet une resulta rapide sur un immense jeu de données
def GradientDescentStochastique(d, bias, weights, pas, courseUse, house):
    lignes = list(range(len(d["First Name"])))
    random.shuffle(lignes)
    cout = 0
    for ligne in lignes:
        data = [d[course][ligne] for course in courseUse]
        prediction_value = prediction(data, bias, weights,courseUse)
        correct = (d["Hogwarts House"][ligne] == house)
        error = prediction_value - correct
        h = min(max(prediction_value, 1e-15), 1 - 1e-15)
        cout += correct * math.log(h) + (1 - correct) * math.log(1 - h)
        for i, course in enumerate(courseUse):
            weights[course] = weights[course] - pas * (error * data[i])
        bias = bias - pas * (error)
    print("House:", house, " Coût:", -cout / len(lignes))
    return bias


def main(filename):
    d = parser(filename)
    courseUse = paser_to_unuseful_stuff(d)
    complets = [ligne for ligne in range(len(d["Hogwarts House"]))
                if all(d[course][ligne] is not None for course in courseUse)]
    d = {col: [d[col][ligne] for ligne in complets]
         for col in courseUse + ["Hogwarts House", 'First Name']}
    stats = {}
    for course in courseUse:
        d[course], mean, stdv = standardization(d[course])
        stats[course] = (mean, stdv)
    houses = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]
    biais = {house: 0 for house in houses}
    pas = 0.1
    weights = {house: {course: 0 for course in courseUse} for house in houses}
    for i in range(10000):
        for house in houses:
            biais[house] = GradientDescent(d, biais[house], weights[house], pas, courseUse, house)
    write(biais, weights, stats)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python logreg_train.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    main(filename)

