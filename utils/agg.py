from tqdm import tqdm
import pandas as pd
import numpy as np
import faiss
import math
import networkx as nx
import matplotlib.pyplot as plt

def agg(LightFM_rec, Collab_filt_rec, PureSVD_rec, indices_graph, weight=[0.5, 0.35, 0.15]):
    id_film, res = [], []
    for dist, indice in indices_graph:
        id_film.append(indice)
    three_alg = [LightFM_rec, Collab_filt_rec, PureSVD_rec]
    for i in range(len(id_film)):
        summ = 0
        for j in range(3):
            summ += three_alg[j][id_film[i] - 1] * weight[j]
        res.append((summ, id_film[i]))
    return sorted(res)[::-1]
