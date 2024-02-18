import plotly.express as px, pandas as pd, numpy as np, random, csv
def read_file(file_path: str, remove_first_line = True) -> list: # this function reads a csv file when given the file path
    with open(f"/Users/nchen26/Code/kitchen/ucc/Y10Coding/DesigningData/Data/{file_path}.csv", newline = '') as cd:
        reader = csv.reader(cd)
        return list(reader)[1:] if remove_first_line else list(reader)
covid_data = read_file("coviddata")
social_data = read_file("socialdiablo")
university_data = read_file("universitystudents")
filler = lambda N: [random.randint(1, 15) for _ in range(5*N)] # this acts as a "filler" to the graph generating random data to fill in the radar chart
group = lambda N: np.repeat([i for i in range(10, 10+N)], 5) # this list helps pandas + plotly classify the different series
theta = lambda N: ['IAT Score (%)','Device Use Frequency (33%)','Average Screen Time (25%)', '# of devices (67%)', 'Possible Mental Disorder (PMD, 0.1%)'] * N # the axis titles
class person: # stores information for individual
    def __init__(self, id, age=-1, gender=-1, IAT=-1, device_use_freq=-1, avg_screen_time=-1, num_of_devices=-1, PMD=-1):
        self.id = id
        self.age = age
        self.gender = gender
        self.IAT = IAT
        self.device_use_freq = device_use_freq
        self.avg_screen_time = avg_screen_time
        self.num_of_devices = num_of_devices
        self.PMD = PMD
class age: # stores information for each age group
    def __init__(self):
        self.IAT = self.dataset()
        self.device_use_freq = self.dataset()
        self.avg_screen_time = self.dataset()
        self.num_of_devices = self.dataset()
        self.PMD = self.dataset()
    class dataset: # stores a total count and a count, helps calculate the average
        total = 0
        count = 0
        def add(self, N): # add to this dadaset
            self.total += N
            self.count += 1
        def avg(self) -> float: # find the average
            return self.total/(self.count if self.count != 0 else 1)
data = [age() for _ in range(30)]
filtered = [[0]*5 for _ in range(30)]
for p in covid_data: # looping through covid_data[] 
    del p[65], p[4], p[-1]
    p = list(map(int, p))
    # id, age, gender, IAT, device_use_freq, avg_screen_time, num_of_devices, PMD
    s = person(p[0], p[3], p[2], p[63], p[11], p[13], p[10], p[19]*25)
    data[s.age].IAT.add(s.IAT)
    data[s.age].device_use_freq.add(s.device_use_freq)
    data[s.age].avg_screen_time.add(s.avg_screen_time)
    data[s.age].num_of_devices.add(s.num_of_devices)
    data[s.age].PMD.add(s.PMD)
for a in range(30): # creates filtered data with an adjustment factor so each graph fits in the radar graph range
    filtered[a][0] = (data[a].IAT.avg())/45
    filtered[a][1] = (data[a].device_use_freq.avg())/3
    filtered[a][2] = (data[a].avg_screen_time.avg())/4
    filtered[a][3] = (data[a].num_of_devices.avg())/1.5
    filtered[a][4] = (data[a].PMD.avg())/1000
def usableData(N) -> list: # complies data for pd.Dataframe
    ret = []
    for a in range(6, 6+N):
        ret += filtered[a]
    return ret
def color_discrete_map(N): # generates the colors for different age groups
    ans = {}
    color_continuous_scale = ['#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600']
    for j in [i for i in range(10, 10+N)]:
        idx = random.randint(0, len(color_continuous_scale)-1)
        ans[j] = color_continuous_scale[idx]
        color_continuous_scale.pop(idx)
    return ans
N = 6
df = pd.DataFrame(dict(value = usableData(N), variable = theta(N), group = group(N)))
fig = px.line_polar(df, r = 'value', theta = 'variable', line_close = True, color = 'group', color_discrete_map=color_discrete_map(N))
fig.update_traces(fill = 'toself', opacity=0.4) # change the opacity
fig.update_layout(polar=dict(radialaxis=dict(range=[0.45, 0.95]))) # change the scale of the graph
fig.show()