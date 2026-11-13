from logreg_train import prediction, parser, standardization
import sys, math

def parserFileWeight(filename):
    weights = {}
    bias = {}
    stats = {}
    courseUse = []
    with open(filename, 'r') as f:
        for line in f:
            key, value = line.strip().split('=', 1)
            prefix, kind = key.rsplit('_', 1)
            value = float(value)

            if kind == "bias":
                bias[prefix] = value
            elif kind == "weight":
                house, course = prefix.split('_', 1)
                weights.setdefault(house, {})[course] = value
                if course not in courseUse:
                    courseUse.append(course)
            elif kind == "mean":
                stats.setdefault(prefix, [0, 0])[0] = value
            elif kind == "std":
                stats.setdefault(prefix, [0, 0])[1] = value
    return weights, courseUse, bias, stats

def write_prediction(predictions):
    with open("../ressources/houses.csv", 'w') as f:
        f.write("Index,Hogwarts House\n")
        for p in predictions:
            f.write(f"{p['index']},{p['house']}\n")

def test(filename, filenameSolu):
    err = 0
    total =0
    with open(filename, 'r') as f:
        with open(filenameSolu, 'r') as s:
            lines = f.readlines()[1:]
            total = len(lines)
            lineSolu = s.readlines()[1:]
            for i, (line, sol) in enumerate(zip(lines, lineSolu)):
                l = line.split(',')[1].strip()
                s = sol.split(',')[1].strip()
                if l != s:
                    print(f"Mismatch at line {i + 2}: predicted '{l}', expected '{s}'")
                    err+=1
    print(total, err)
    print("Pourcentage de réussite", (total - err) * 100 / total)

def main(filename, filenameWeights):
    d = parser(filename)
    predictions_temp = []
    predictions = []
    weights, courseUse, biais, stats = parserFileWeight(filenameWeights)
    for course in courseUse:
        mean, stdv = stats[course]
        d[course] = [0.0 if v is None else (v - mean) / stdv for v in d[course]]
    houses = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]
    pas = 0.1
    for ligne in range(len(d["First Name"])):
        data = [d[course][ligne] for course in courseUse]
        for house in houses:
            predictions_temp.append(prediction(data, biais[house], weights[house], courseUse))
        moreLikely= max(predictions_temp)
        predictions.append({"index": int(d["Index"][ligne]), "house": houses[predictions_temp.index(moreLikely)]})
        predictions_temp = []
    write_prediction(predictions)
    test("../ressources/houses.csv", filename)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python describe.py <filename>")
        sys.exit(1)
    main( sys.argv[1], sys.argv[2])

