import numpy as np
import math
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


f = open("test-example-n4.txt", "r")

#print(f.read())
number_of_cities=4
city_cordinates=np.zeros((number_of_cities, 2), dtype=np.float64)
dist_matrix=np.zeros((number_of_cities, number_of_cities), dtype=np.float64)
#storing cordinates of city nodes into a number of cities * 2 array
line=f.readline()
while(line.strip() != ''):
    
    if "NODE_COORD_SECTION" in line:
        for i in range(number_of_cities):
            line=f.readline()
            a = line.split()
            city_cordinates[i][0] = float(a[1].strip())
            city_cordinates[i][1] = float(a[2].strip())
        break
    line=f.readline()
    
for i in range(number_of_cities):
    for j in range(number_of_cities):
        if(i!=j):
           # print(city_cordinates[i])
            #print(city_cordinates[j])
            dist_matrix[i][j] = euclidean_distance(city_cordinates[i], city_cordinates[j])

print(dist_matrix)
    