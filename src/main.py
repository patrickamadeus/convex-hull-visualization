# base library
import pandas as pd  
import matplotlib.pyplot as plt

# convex hull implementation library
from lib import convex_hull  

# datasets property
from sklearn import datasets
data_sets = [
    (datasets.load_iris(), "Iris Plants Dataset"),
    (datasets.load_wine(), "Wine Recognition Dataset"),
    (datasets.load_breast_cancer(), "Breast Cancer Wisconsin (Diagnostic) Dataset"),
]


#------------- Choose Dataset -----------------#
print('''
Choose any classification dataset from Toy Datasets properties as listed below
1. Iris Plants Dataset
2. Wine recognition dataset
3. Breast cancer wisconsin (diagnostic) dataset\n
''')
data_sets_choice = int(input("Enter the dataset number : "))
data = data_sets[data_sets_choice - 1][0]



#------------- Mapping data Feature and Label -----------------#
df = pd.DataFrame(data.data, columns=data.feature_names)
df['Target'] = pd.DataFrame(data.target)



#------------- Enumerate Target Label from Dataset -----------------#
n_target = len(df.Target.value_counts())
d_target = {}
for i in range(n_target):
    d_target[i] = (df.Target.value_counts().index[i])
print()



#------------- Picking 2 of Available Column(s) -----------------#
idx = 0
msg = ""
for i in range(len(df.columns)):
    msg += (str(i+1)+". "+str(df.columns[i]) + "\n")
print("%s dataset have %d columns which enumerated as below : " %(data_sets[data_sets_choice - 1][1], len(df.columns)))
print(msg)
idX,idY = int(input("Pick column 1 to plot : ")),int(input("Pick column 2 to plot : "))
while idX == idY:
    print("Please choose different column!")
    idY = int(input("Pick column 2 to plot : "))
x,y = df.columns[idX-1],df.columns[idY-1]



#------------- Gather Points for Chosen Columns -----------------#
d_points = {}
for i in d_target:
    d_points[i] = [(df[x].values[j] , df[y].values[j]) for j in range(len(df[x])) if df.Target.values[j] == i]



#------------- Quick Sort implementation for point sets -----------------#
def quick_sort(points):
    if len(points) <= 1:
        return points
    else:
        pivot = points[0]
        less = [point for point in points[1:] if (point[0] < pivot[0]) or (point[0] == pivot[0] and point[1] < pivot[1])]
        greater = [point for point in points[1:] if (point[0] > pivot[0]) or (point[0] == pivot[0] and point[1] >= pivot[1])]
        return quick_sort(less) + [pivot] + quick_sort(greater)
    
for key in d_points:
    d_points[key] = quick_sort(d_points[key])



#------------- Gather Convex Hull Point(s) for each target ---------------#
hull_points = {}
for i in range(n_target):
    d = convex_hull(d_points[i])
    hull_points[i] = convex_hull(d_points[i])



#------------- Final Scatterplot with Convex Hull visualization ---------------#
# color pallete for plotting use (assumption max target label is 8)
color_pallete = ["blue","green","red","purple","magenta","yellow","black","white"]

# figure size
f = plt.figure()
f.set_figwidth(7.5)
f.set_figheight(5)

# scatter plot for points
for i in d_points:
    x, y = [pts[0] for pts in d_points[i]],[pts[1] for pts in d_points[i]]
    plt.scatter(x,y,c = color_pallete[i], label = data.target_names[i] ,s=20)

# linear line plotting for convex hull
for i in hull_points:
    size = len(hull_points[i])
    for j in range(len(hull_points[i])):
        plt.plot([hull_points[i][j % size][0], hull_points[i][(j + 1)% size][0]], [hull_points[i][j % size][1], hull_points[i][(j + 1)% size][1]] , c = color_pallete[i], linewidth = 0.75)

# axis label, title, legend
plt.title("Convex Hull Visualization for %s" %(data_sets[data_sets_choice - 1][1]))
plt.xlabel(df.columns[int(idX) - 1])
plt.ylabel(df.columns[int(idY) - 1])
plt.legend()

plt.show()