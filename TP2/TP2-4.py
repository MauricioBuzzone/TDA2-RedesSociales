from multiprocessing import Process
from statistics import mean

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import random
import math

random.seed(44)
colors = ['steelblue', 'orange', 'green']

def run_simulation(process_id, G, q, p, simulations):
    print(f'[{process_id}]: start')
    iterations = 200
    epidemic = 0
    for i in range(simulations):
        print(f'[{process_id}]: simulation {i}')
        infectious = max(nx.degree_centrality(G))#random.randint(0,n)

        sus, inf,rec = simulate_virus(process_id,G,infectious, q, p,iterations)

        if rec[-1] > n*0.3:
            epidemic +=1

        x = list(range(0,  iterations+1))
        plt.plot(x, sus, color=colors[0])
        plt.plot(x, inf, color=colors[1])
        plt.plot(x, rec, color=colors[2])

    legend_lines = [plt.Line2D([0], [0], color=color, linewidth=3) for color in colors]
    plt.legend(legend_lines, ['Susceptible', 'Infected', 'Recovered'])
    plt.xlabel('Iteraciónes')
    plt.ylabel('Cantidad de nodos')
    plt.title('Modelo SIR apilicado a '+ str(process_id))
    plt.show()
    print(f'[{process_id}]: End | result: epidemic: {epidemic}')

def simulate_virus(process_id,G, infectious, q, p, iter=100):

    susceptible = [node for node in G.nodes if node != infectious]
    infected = {}
    recovered = []
    
    infected[infectious] = infectious

    susceptible_amount = []
    infected_amount = []
    recovered_amount = []

    susceptible_amount.append(len(G.nodes) - len(infected))
    infected_amount.append(len(infected))
    recovered_amount.append(0)

    
    for i in range(iter):
        new_susceptible = []
        new_infected = {}
        #print(f'[{process_id}]: Iteración {i}')

        for sus in susceptible:
            neighbors = [n for n in G.neighbors(sus)]
            infectados = [node for node in neighbors if node in infected] 
            d = len(infectados)

            if random.uniform(0,1) < 1 - (1-q)**d :
                infected[sus] = sus
            else:
                new_susceptible.append(sus)

        for inf in infected.keys():
            if random.uniform(0,1) < p:
                recovered.append(inf)
            else:
                new_infected[inf] = inf

        susceptible = new_susceptible
        infected = new_infected

        susceptible_amount.append(len(G.nodes) - len(infected) - len(recovered))
        infected_amount.append(len(infected))
        recovered_amount.append(len(recovered))

    return susceptible_amount, infected_amount, recovered_amount
            
# n = Cant. nodos
# d = Grado promedio
# q = prob de contagiar

n = 6411 # 226
d = 52.1 # 25
q = 0.006 # S --> I
p = 0.05 # I --> R

#n = 226
#d = 25

df = pd.read_csv('marvel.csv', delimiter = ' ')

G = nx.Graph()
# Agrega nodos y aristas al grafo
for index, row in df.iterrows():
    G.add_edge(row['SOURCE'], row['DEST'], weight=row['WEIGHT'])



# Erdos Renyi
# G_erdos_renyi = nx.erdos_renyi_graph(n,d/n)

# Preferential Attachment
# G_preferential_attachment = nx.barabasi_albert_graph(n, round(d/2))

'''
d_2 = [degree**2 for node,degree in G_erdos_renyi.degree]
print(f'Erdos Renyi R0 = {q * d  * (mean(d_2))/(d**2)}')

d_2 = [degree**2 for node,degree in G_preferential_attachment.degree]
print(f'Preferential Attachment R0 = {q * d * (sum(d_2)/len(d_2))/(d**2)}')
'''
process1 = Process(target=run_simulation, args=("Marvel", G, q, p, 100))
#process2 = Process(target=run_simulation, args=("Preferential Attachment", G_preferential_attachment, q, p, 100))

# Iniciar procesos
process1.start()
#process2.start()

# Esperar a que ambos procesos terminen
process1.join()
#process2.join()


"""
degree_dict = dict(G_preferential_attachment.degree(G_preferential_attachment.nodes()))

# Encuentra el nodo con el grado más alto
max_degree_node = max(degree_dict, key=degree_dict.get)"""
