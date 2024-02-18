import matplotlib as mpl, numpy as np, csv, matplotlib.pyplot as plt
def read_file(file_path: str, remove_first_line = True) -> list: # this function reads a csv file when given the file path
    with open(f"/Users/nchen26/Code/kitchen/ucc/Y10Coding/DesigningData/Data/{file_path}.csv", newline = '') as cd:
        reader = csv.reader(cd)
        return list(reader)[1:] if remove_first_line else list(reader)
university_data = read_file("universitystudents")
data = [[] for _ in range(101)]
for p in university_data: # loop through the csv
    total = 0
    for i in list(map(int, p[22:49])): # taking values from p[22:49]
        if i != 99:
            total += i
    internet_usg = int(p[1])
    data[internet_usg].append(total)
avgs = {}
for usg in range(101):
    if len(data[usg]) != 0:
        avgs[usg] = sum(data[usg]) / len(data[usg]) # calculating average if its not 0
fig = plt.figure(figsize=(6,6)) # Creating figure
ax = fig.add_subplot(111)
ax.set_facecolor('xkcd:black') # make the graph dark mode
textColor = 'xkcd:very light purple' # this is one of the main colors I am going to use in my dark mode template
fig.patch.set_facecolor('xkcd:black')
ax.tick_params(axis='x', colors=textColor) # change tick color so it shows in dark mode
ax.tick_params(axis='y', colors=textColor)
ax.spines['left'].set_color(textColor) # change spine color so it shows in dark mode
ax.spines['bottom'].set_color(textColor)
ax.text(0.1, 0.85, 'Mental health on\na scale of 0-60,\n60 being worst', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, bbox = {'facecolor': 'black', 'edgecolor': textColor}, size=13, fontweight="bold", color=textColor, fontname="Silom") # Opacity correlation textbox
plt.plot(list(avgs.keys()), list(avgs.values()), linestyle='-', color=textColor)
plt.title('Average Sum of Values vs. Internet Usage', color=textColor, fontweight="bold", fontname="Silom")
plt.xlabel('Internet Usage (% of day used online)', color=textColor, fontweight="bold", fontname="Silom")
plt.ylabel('Mental Health', color=textColor, fontweight="bold", fontname="Silom")
plt.grid(False)
plt.show()