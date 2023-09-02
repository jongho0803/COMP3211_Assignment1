import numpy as np
import pandas as pd


def split_X_y(file_name):
    data = pd.read_csv('../assign1-data_python3/' + file_name, header=None)
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1:].values

    return X, y


def augment(X):
    temp = np.ones((len(X), len(X[0]) + 1))
    temp[:, :-1] = X

    return temp


def initialize(num_genes, num_weights):
    
    return np.random.uniform(low=-4, high=4, size=(num_genes, num_weights))


def fitness(X, y, genes):
    scores = []
    y = y.reshape(1, -1)[0]

    for g in genes:
        diff = np.matmul(X, g)

        a = (diff >= 0)
        b = y.reshape((1, -1))

        scores.append(np.sum(a==b))

    return scores


def copy(index, genes, num_top50):
    top50 = index[:int(num_top50)]

    return genes[top50]


def crossover(high_quality_genes, num_rest_genes):
    children = []

    while(len(children) < num_rest_genes):
        # Create random numbers
        t = np.arange(len(high_quality_genes[0]))
        np.random.shuffle(t)
        t = t[:2]

        #Pick two genes as mother and father randomly
        mother = high_quality_genes[t[0]].copy()
        father = high_quality_genes[t[1]].copy()

        #Compare every element
        compared_element = np.array(mother) == np.array(father)

        if np.all(compared_element):
            pass
        else:
            child = []

            #Randomly pick gene from mother or father for crossover
            for i in range(len(mother)):
                if np.random.randint(2):
                    child.append(mother[i])
                else:
                    child.append(father[i])

            children.append(child)

    return children


def mutation(genes):
    set_num = np.random.randint(len(genes))
    part_index = np.random.randint(len(genes[0]))
    genes[set_num][part_index] = genes[set_num][part_index] * (np.power(-1, i) + 0.5)

    return genes

num_genes = 1000
np.random.seed(663)

#Load data and split
X, y = split_X_y('gp-training-set.csv')

#Augment X to X+1 to deal with theta
X = augment(X)

#Initialize
genes = initialize(num_genes, len(X[0]))

for i in range(100):
    # fitness
    f = fitness(X, y, genes)
    # reversed order index
    rank_index = np.argsort(f)[::-1][:]

    print('accuracy = ', f[rank_index[0]])
    print('Perceptron = ', genes[rank_index[0]])
    print('')

    #If top fitness is high enough, stop
    if f[rank_index[0]] > 98:
        break

    #Copy top 50% of the gene
    high_quality_genes = copy(rank_index, genes, num_genes*0.50)

    #Create child genes by combining top 50% genes and crossovered genes
    genes[:len(high_quality_genes)] = high_quality_genes
    genes[len(high_quality_genes):] = crossover(high_quality_genes, num_genes-len(high_quality_genes))

    #Mutation
    genes = mutation(genes)



print('Final score, [Weights, -Theta]')
print(f[rank_index[0]])
print(genes[rank_index[0]])