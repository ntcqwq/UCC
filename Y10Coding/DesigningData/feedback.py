# CODE FOR D2, NOT FOR C
import matplotlib as mpl, numpy as np, csv, matplotlib.pyplot as plt, pandas as pd 
def read_file(file_path: str, remove_first_line = True) -> list: # this function reads a csv file when given the file path
    with open(f"/Users/nchen26/Code/kitchen/ucc/Y10Coding/DesigningData/Data/{file_path}.csv", newline = '') as cd:
        reader = csv.reader(cd)
        return list(reader)[1:] if remove_first_line else list(reader)
feedback_data = read_file("feedback")
N = len(feedback_data)
data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
for p in feedback_data:
    data[0][0] += int(p[2])/N
    data[1][0] += int(p[3])/N
    data[2][0] += int(p[4])/N
    data[0][1] += int(p[5])/N
    data[1][1] += int(p[6])/N
    data[2][1] += int(p[7])/N
    data[0][2] += int(p[8])/N
    data[1][2] += int(p[9])/N
    data[2][2] += int(p[10])/N
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center',
                 Bbox = dict(facecolor = 'red', alpha =.8))
width = 0.2
def addlabels(x, y):
    for i in range(len(x)):
        plt.text(x[i], y[i], f'{y[i]:.2f}', ha='center', va='bottom', color='black')
x = np.arange(3) 
plt.bar(x-0.2, data[0], width, color='blue') 
plt.bar(x, data[1], width, color='orange') 
plt.bar(x+0.2, data[2], width, color='pink') 
addlabels(x - 0.2, data[0])
addlabels(x, data[1])
addlabels(x + 0.2, data[2])
plt.xticks(x, ['2D Scatter', 'Radar', 'Line']) 
plt.xlabel("Chart") 
plt.ylabel("Score") 
plt.legend(['Informative', 'Aesthetics', 'Creativity']) 
plt.show() 
