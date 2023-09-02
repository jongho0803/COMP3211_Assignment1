import numpy as np
import pandas as pd

def split_X_Y(file_name):
    data = pd.read_csv('../../assign1-data_python3/' + file_name, header=None)
    X = data.iloc[:, :-1].values
    Y = data.iloc[:, -1].values

    return X, Y

def augment(X):
    temp = np.ones((len(X), len(X[0]) + 1))
    temp[:, 1:] = X

    return temp

def find_perceptron(set, label):
    weight = np.zeros(len(set[0]))
    check = np.zeros(len(set))

    while (1):
        for i in range(len(set)):
            sigma = 0
            for j in range(len(set[0])):
                sigma += set[i][j] * weight[j]
            
            if (sigma >= 0):
                outcome = 1
            else:
                outcome = 0

            if(outcome == label[i]):
                check[i] = 1
            else:
                for j in range(len(set[0])):
                    weight[j] += (label[i] - outcome) * set[i][j] 
                check[i] = 0
        
        if (sum(check) == len(check)):
            break

    weight[0] *= -1

    return weight


north_set, north_label = split_X_Y('north.csv')
north_set = augment(north_set)
north_perceptron = find_perceptron(north_set, north_label)

west_set, west_label = split_X_Y('west.csv')
west_set = augment(west_set)
west_perceptron = find_perceptron(west_set, west_label)

south_set, south_label = split_X_Y('south.csv')
south_set = augment(south_set)
south_perceptron = find_perceptron(south_set, south_label)

east_set, east_label = split_X_Y('east.csv')
east_set = augment(east_set)
east_perceptron = find_perceptron(east_set, east_label)