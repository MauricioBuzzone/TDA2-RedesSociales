import itertools

from multiprocessing import Process
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import random
import math

def transform(value, original_interval=(1, 5), destination_interval=(-1, 1)):
    # Unpack the ends of the original and destination intervals
    a, b = original_interval
    c, d = destination_interval

    # Calculate the slope and y-intercept
    m = (d - c) / (b - a)
    intercept = c - m * a

    # Apply the linear transformation
    result = m * value + intercept

    return result

gamma1 = 0.5
gamma2 = 0.5

df = pd.read_csv('ratings_electronics.csv')

# Cada usuario tiene una cierta noción de justicia (fairness) → F(u) ∈ [0,1]
# Cada producto tiene un "valor" → G(p) ∈ [-1,1]
# Los ratings tienen una fiabilidad → R(u,p) ∈ [0,1]
users = dict.fromkeys(df['USER_ID'], 1)
products = dict.fromkeys(df['PRODUCT_ID'], 1)
ratings = dict.fromkeys(zip(df['USER_ID'], df['PRODUCT_ID']), 1)

G = nx.DiGraph()
# Agrega nodos y aristas al grafo
for index, row in df.iterrows():
    G.add_edge(row['USER_ID'], row['PRODUCT_ID'], weight=row['SCORE'])

max_diff = 0
i = 0
while max_diff >= 0.00005 or i <= 1:
    print(f'[Iteration {i}]: max_diff: {max_diff}')
    max_diff = 0
    for user in users.keys():
        old = users[user]
        d = G.degree(user)
        reviews = G.out_edges(user)
        users[user] = sum(ratings[review] for review in reviews)/d

        max_diff = max(max_diff, abs(old - users[user]))


    for product in products:
        d = G.degree(product)
        reviews = G.in_edges(product)
        products[product] = sum(ratings[review] * transform(G.get_edge_data(*review)['weight']) for review in reviews)/d

    for review in G.edges:
        user, product = review
        score = transform(G.get_edge_data(*review)['weight'])
        ratings[review] = 1/(gamma1+gamma2) * ( gamma1 * users[user] + gamma2 * (1 - abs(score - products[product])/2))

    i+=1

with open('justos.csv', 'w') as justos_file, open('maliciosos.csv', 'w') as malisiosos_file:
    for u in users.items():
        user_id, F_u = u[0], u[1]

        if F_u >= 0.9 and G.degree(user_id) >= 10:
            justos_file.write(f'User: {user_id} F(u): {F_u}\n')
        elif F_u <= 0.2 and G.degree(user_id) >= 5:
            malisiosos_file.write(f'User: {user_id} F(u): {F_u}\n')
