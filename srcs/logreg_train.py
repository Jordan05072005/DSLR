from describe import std, parser
from histogram import COURSES, to_float
from scatter_plot import paired, coefPearson
import sys, math
from itertools import combinations


THRESHOLD_STANDARD_DEVIATION = 5
THRESHOLD_COEF_PEARSON = 0.8

def paser_to_unuseful_stuff(d):
    coursesUse = COURSES
    for course in coursesUse:
        val = std(to_float(d[course]))
        if (val < THRESHOLD_STANDARD_DEVIATION):
            coursesUse.remove(course)
    for a, b in combinations(COURSES, 2):
        xs, ys = paired(d[a], d[b])
        coef = coefPearson(xs, ys)
        if abs(coef) > THRESHOLD_COEF_PEARSON:
            coursesUse.remove(a or b)
    return coursesUse

def sigma(z):
    return 1 / (1 + math.exp(-z))

def prediction(bias, weights, arr, coursesUse):
    for i, value in enumerate(arr):
        biais += (value * weights[coursesUse[i]])
    return sigma(biais)

# [{}]

def GradientDescent(filename):
    d = parser(filename)
    courseUse = paser_to_unuseful_stuff(d)
    biais = 0
    weights = {course: 0 for course in courseUse}
    errors = []
    pas = 0.1
    for ligne in range(len(d["First Name"])):
        arr = [ d[course][ligne] for course in courseUse]
        prediction_value = prediction(biais, weights, arr, courseUse)
        error = prediction - True
        for course in courseUse:
            error
        for course in courseUse:
            meanErrorNote = sum( err.get("note") * err.get("error") for err in errors) / len(errors)
            meanError = sum( err.get("error") for err in errors) / len(errors)
            weights[course] = (weights[course] - pas) * meanErrorNote
            bias = (bias - pas) * meanError
    print(weights, "and", bias)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python describe.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    GradientDescent(filename)

