from multiprocessing import Process
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import random
import math

random.seed(44)
def run_simulation(process_id, G, infectious, q, iterations):
    print(f'[{process_id}]: start')
    sus, inf,rec = simulate_virus(process_id,G,infectious,q,iterations)

    x = list(range(0, iterations+1))
    plt.plot(x, sus, label='Susceptible')
    plt.plot(x, inf, label='Infected')
    plt.plot(x, rec, label='Recovered')

    plt.xlabel('Iteracion')
    plt.ylabel('Cant de nodos')
    plt.title('Modelo SIR apilicado a '+ str(process_id) +' '+ 'q = '+ str(q))
    plt.legend()
    plt.show()
    print(f'[{process_id}]: End')

def simulate_virus(process_id,G, infectious, q, iter=100):

    susceptible_amount = []
    infected_amount = []
    recovered_amount = []

    
    recovered = {}
    infected = {}
    infected[infectious] = infectious

    susceptible_amount.append(len(G.nodes) - len(infected))
    infected_amount.append(len(infected))
    recovered_amount.append(0)
    
    for i in range(iter):
        new_infected = {}
        print(f'[{process_id}]: Iteracion {i}')

        for inf in infected:
            neighbors = [edges[1] if edges[0] == inf else edges[0] for edges in G.edges if inf in edges]
                            
            for node in neighbors:
                if node not in recovered and node not in infected and node not in new_infected:
                    if random.uniform(0,1) < q:
                        #print(f'[Iteracion {i}]: {inf} infecto a {node}')
                        new_infected[node] = node

            if random.uniform(0,1) < q:
                #print(f'[Iteracion {i}]: {inf} sigue infectado')
                new_infected[inf] = inf
            else:
                #print(f'[Iteracion {i}]: {inf} se recupero')
                recovered[inf] = inf

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
q = 0.015

# Erdos Renyi
G_erdos_renyi = nx.erdos_renyi_graph(n,d/n)
infected_erdos_renyi = random.randint(0,n)

# Preferential Attachment
G_preferential_attachment = nx.barabasi_albert_graph(n, round(d/2))
infected_preferential_attachment = random.randint(0,n)

process1 = Process(target=run_simulation, args=("Erdos Renyi", G_erdos_renyi, infected_erdos_renyi, q, 20))
process2 = Process(target=run_simulation, args=("Preferential Attachment", G_preferential_attachment, infected_preferential_attachment, q, 20))

# Iniciar procesos
process1.start()
process2.start()

# Esperar a que ambos procesos terminen
process1.join()
process2.join()


"""
degree_dict = dict(G_preferential_attachment.degree(G_preferential_attachment.nodes()))

# Encuentra el nodo con el grado más alto
max_degree_node = max(degree_dict, key=degree_dict.get)"""
