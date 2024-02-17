import numpy as np, matplotlib.pyplot as plt, matplotlib as mpl, random, csv
with open('coviddata.csv') as file:
    covid_reader = list(csv.reader(file))[1:] # reading the file coviddata.csv
covid_reader.sort(key = lambda x: int(x[0])) # to make data easier to read, sorting people by their "id". This "id" is a unique key that we can use
data = {} # we are going to store all data analysed in a dictionary
for person in covid_reader:
    del person[65], person[4], person[-1] # remove bad data
    person = list(map(int, person)) # convert [String] to [Int]
    pid, gender, age, primary_electronic_devices, device_use_frequency_covid, device_use_frequency_before, duration_per_day_covid, duration_per_day_before, degree_of_addiction_covid, degree_of_addiction_before, IAT_total, anxiety_classification_3, depression_classification_3, stress_classification_3 = person[0], person[2], person[3], person[10], person[11], person[12], person[13], person[14], person[19], person[20], person[63], person[68], person[69], person[70] # extract useful data
    data[pid] = {'gender': 'blue' if gender == 1 else 'xkcd:fuchsia', 'age': age, 'devices': primary_electronic_devices, 'use_freq': device_use_frequency_covid, 'use_increase': device_use_frequency_covid - device_use_frequency_before, 'duration_avg': duration_per_day_covid, 'duration_increase': duration_per_day_covid - duration_per_day_before} # append them in a dictionary 
x, y, z, c, a = [], [], [], [], [] # these 5 "variables" that determine xpos, ypos, size, color, and transparency for males
x2, y2, z2, c2, a2 = [], [], [], [], [] # these 5 "variables" that determine xpos, ypos, size, color, and transparency for females
for i in data:
    # for each data point, append them into corresponding axis, also add a bit of randomness cus why not
    if data[i]['gender'] == "blue":
        x.append(data[i]['age'] + random.choice([-0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4]))
        y.append(data[i]['duration_avg'] + random.choice([-0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4]))
        z.append(data[i]['use_freq']*150)
        c.append(data[i]['gender'])
        a.append(data[i]['devices']/5)
    else:
        x2.append(data[i]['age'] + random.choice([-0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4]))
        y2.append(data[i]['duration_avg'] + random.choice([-0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4]))
        z2.append(data[i]['use_freq']*150)
        c2.append(data[i]['gender'])
        a2.append(data[i]['devices']/5)
fig = plt.figure(figsize=(6,6)) # Creating figure
ax = fig.add_subplot(111)
ax.set_facecolor('xkcd:black') # make the graph dark mode
fig.patch.set_facecolor('xkcd:black')
textColor = 'xkcd:very light purple' # this is one of the main colors I am going to use in my dark mode template
malescatter = ax.scatter(x, y, s=z, c=c, alpha=a, marker='o', label='Male') # plot axis for males
femalescatter = ax.scatter(x2, y2, s=z2, c=c2, alpha=a2, marker='o', label='Female') # plot axis for females
ax.tick_params(axis='x', colors=textColor) # change tick color so it shows in dark mode
ax.tick_params(axis='y', colors=textColor)
ax.spines['left'].set_color(textColor) # change spine color so it shows in dark mode
ax.spines['bottom'].set_color(textColor)
ax.text(0.1, 0.05, 'Opacity correlates to\nNumber of devices', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, bbox = {'facecolor': 'black', 'edgecolor': textColor}, size=10, fontweight="bold", color=textColor, fontname="Silom") # Opacity correlation textbox
ax.text(0.1, 0.125, 'Size correlates to\nFrequency of device use', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, bbox = {'facecolor': 'black', 'edgecolor': textColor}, size=9, fontweight="bold", color=textColor, fontname="Silom") # Size correlation textbox
legend = plt.legend(prop={'size': 14, 'weight': "bold", 'family': "Silom"}, loc='upper left')
legend.get_texts()[0].set_color("blue")
legend.get_texts()[1].set_color("xkcd:fuchsia") 
legend.get_frame().set_facecolor('black')
legend.get_frame().set_edgecolor(textColor)
plt.title("Age vs Average Duration on electronic devices during COVID", color=textColor, fontweight="bold", fontname="Silom")
plt.xlabel("Age (Years)", color=textColor, fontweight="bold", fontname="Silom") # x and y labels
plt.ylabel("Duration (Hours)", color=textColor, fontweight="bold", fontname="Silom")
plt.show() # show plot