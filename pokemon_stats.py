import csv
import random
import math
import numpy as np
import matplotlib.pyplot as plt

def load_data(filepath):
    reader = csv.DictReader(open(filepath))
    reader = list(reader)[0:20]
    for row in reader:
        row.pop('Generation')
        row.pop('Legendary')
        row['#'] = int(row['#'])
        row['Total'] = int(row['Total'])
        row['HP'] = int(row['HP'])
        row['Attack'] = int(row['Attack'])
        row['Defense'] = int(row['Defense'])
        row['Sp. Atk'] = int(row['Sp. Atk'])
        row['Sp. Def'] = int(row['Sp. Def'])
        row['Speed'] = int(row['Speed'])
    return reader

def calculate_x_y(stats):
    return (stats['Attack']+stats['Sp. Atk']+stats['Speed'], 
        stats['Defense']+stats['Sp. Def']+stats['HP'])

def hac(dataset):
    # make sure all data are valid
    for d in dataset:
        if math.isnan(d[0]) or math.isnan(d[1]) or math.isinf(d[0]) or math.isinf(d[1]):
            dataset.remove(d)

    l, dis, clu = len(dataset), [], [] # store length, create distance array, and create cluster
    for i in range(l):
        clu.append([i])
        for j in range(l):
            if j+i+1 < l:
                dis.append([i, j+i+1, math.dist(dataset[i],dataset[j+i+1]), 2])
    dis = np.array(dis)
    dis = dis[dis[:,2].argsort()] # sort by the smallest Euclidean distance
    dis_d, clusters = dis, []

    while True:
        if len(clu[len(clu)-1]) == l:
            break
        result = dis_d[0]
        dis_d = np.delete(dis_d, 0, 0)
        # check whether both points in same cluster
        jump_flag = False
        for i in range(len(clu)-1, l-1, -1):
            if (result[0] in clu[i]) and (result[1] in clu[i]):
                jump_flag = True
                break
        if jump_flag:
            continue
        # check whether in cluster
        for i in range(len(clu)-1, l-1, -1):
            if result[0] in clu[i]:
                result[0] = i
            if result[1] in clu[i]:
                result[1] = i
        # exchange direction
        if result[0] > result[1]:
            temp = result[0]
            result[0] = result[1]
            result[1] = temp
        # cluster size
        result[3] = len(clu[int(result[0])]) + len(clu[int(result[1])])
        clusters.append(result)
        clu.append(clu[int(result[0])]+clu[int(result[1])])
        
    return np.array(clusters)

def random_x_y(m):
    r = []
    while m > 0:
        r.append([random.randint(1,360), random.randint(1,360)])
        m -= 1
    return r

def imshow_hac(dataset):
    # make sure all data are valid
    for d in dataset:
        if math.isnan(d[0]) or math.isnan(d[1]) or math.isinf(d[0]) or math.isinf(d[1]):
            dataset.remove(d)

    plt.figure()
    x, y = [], []
    for d in dataset:
        x.append(d[0])
        y.append(d[1])
    plt.scatter(x, y)

    l, dis, clu = len(dataset), [], [] # store length, create distance array, and create cluster
    for i in range(l):
        clu.append([i])
        for j in range(l):
            if j+i+1 < l:
                dis.append([i, j+i+1, math.dist(dataset[i],dataset[j+i+1]), 2])
    dis = np.array(dis)
    dis = dis[dis[:,2].argsort()] # sort by the smallest Euclidean distance
    dis_d, clusters = dis, []

    while True:
        if len(clu[len(clu)-1]) == l:
            break
        result = dis_d[0]
        dis_d = np.delete(dis_d, 0, 0)
        # check whether both points in same cluster
        jump_flag = False
        for i in range(len(clu)-1, l-1, -1):
            if (result[0] in clu[i]) and (result[1] in clu[i]):
                jump_flag = True
                break
        if jump_flag:
            continue
        # plot
        xp = dataset[int(result[0])][0], dataset[int(result[1])][0]
        yp = dataset[int(result[0])][1], dataset[int(result[1])][1]
        # check whether in cluster to update number representation
        for i in range(len(clu)-1, l-1, -1):
            if result[0] in clu[i]:
                result[0] = i
            if result[1] in clu[i]:
                result[1] = i
        # exchange direction
        if result[0] > result[1]:
            temp = result[0]
            result[0] = result[1]
            result[1] = temp
        # cluster size
        result[3] = len(clu[int(result[0])]) + len(clu[int(result[1])])
        clusters.append(result)
        clu.append(clu[int(result[0])]+clu[int(result[1])])
        plt.plot(xp, yp)
        plt.pause(0.1)

    plt.show()

  
if __name__=="__main__":
    pokemons = load_data('Pokemon.csv')
    pokemons_x_y = []
    for row in pokemons:
        pokemons_x_y.append(calculate_x_y(row))
    imshow_hac(pokemons_x_y)