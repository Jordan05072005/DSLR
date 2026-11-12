import matplotlib.pyplot as plt
import numpy as np
import describe as dsc

rng = np.random.normal(size=1000)

items = dsc.parser("../datasets/dataset_train.csv")

for i in items: 
	print(i)
	


fig, (axe1, axe2) = plt.subplots(1, 2)
fig.suptitle("Representation of grades distribution by classes, btwn houses")
# axe1.plot(x, y)



plt.show()

