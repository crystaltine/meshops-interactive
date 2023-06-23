# generate 104 random numbers between 290.5 and 293.5
import random

with open('linebyline_nyc.txt', 'a') as f:
    for i in range(105):
        f.write(f'{round(random.uniform(290.5, 293.5), 2)}\n')