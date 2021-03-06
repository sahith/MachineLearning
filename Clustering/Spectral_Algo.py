#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 02:46:39 2018

@author: sahith
"""

import numpy as np
import math
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def circs():
    X = np.zeros((2, 100))
    y = 0

    i_s = np.arange(0, 2*np.pi, np.pi/25.0)

    for i in i_s:
        X[0, y] = np.cos(i)
        X[1, y] = np.sin(i)
        y += 1

    for i in i_s:
        X[0, y] = 2*np.cos(i)
        X[1, y] = 2*np.sin(i)
        y += 1
    return X

def similarity_matrix(X, sigma):
    n = len(X)
    sim_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1):
            if i == j:
                sim_matrix[i, j] = 1   #Similarity between 2 same rows is 1
            else:
                dist = np.linalg.norm(X[i]-X[j])
                k = (-1 / (2 * (sigma**2))) * (dist**2)
                sim_matrix[i, j] = sim_matrix[j, i] = math.exp(k)
    return sim_matrix
                
            
     
def Laplacian_matrix(A):
    n = len(A)
    D = np.zeros((n, n))  #D is a diagonal matrix with D[i, i]= ´∑j A[i, j]
    for i in range(n):
        k = 0
        for j in range(n):
            k += A[i, j]
        D[i, i] = k
    return D - A
            

def eigen(L):
    return np.linalg.eig(L)

def spectralClustering(sim_matrix):
    K = 2
    L  =  Laplacian_matrix(sim_matrix)
  

    eigenValues, eigenVectors = eigen(L)
    idx = eigenValues.argsort()[0:K]  
    eigenValues = eigenValues[idx]
    V = eigenVectors[:,idx]
    spectral = KMeans(n_clusters=K).fit(V)
    labels = spectral.labels_
    clusters, cluster_centers = clusters_formation(labels, V, K)
    return clusters, labels


def clusters_formation(labels, data, total_clusters):
    clusters = []  #Initilaizing the Clusters 
    cluster_centers = [] #Initilaizing the Clusters centers
    m = total_clusters
    for i in range(m):   #Initilaizing each Cluster Center 
        clusters.append([])
        cluster_centers.append(0)
    n = len(data)
    for i in range(n):
        clusters[labels[i]].append(data[i])
        cluster_centers[labels[i]] = cluster_centers[labels[i]]+data[i]
    for i in range(m):
        cluster_centers[i] = cluster_centers[i]/len(clusters[i])
    return clusters, cluster_centers
    

def loss(clusters, centers):
    n = len(centers)
    loss = 0
    
    for i in range(n): #for each cluster
        cluster_center = centers[i]
        cluster = clusters[i]
        for j in cluster:
            k = np.linalg.norm(cluster_center-j)
            loss += k**2
    return loss
    
    

#Set the DataSet
X = circs() #Concentric Circles dataset is taken as the sample dataset
X =  X.transpose()
sigma = 0.1   #Set the Sigma Value
A = similarity_matrix(X, sigma)


"""
Spectral Algorithm Starts
Given a Similarity Matrix it outputs the clusters by using Spectral Clustering
"""


final_Clusters, labels = spectralClustering(A) #Spectral Clustering(Default Clusters is set to 2)


#Scatter Plot
"""
LABEL_COLOR_MAP = {0 : 'r',
                   1 : 'k',
                   }
label_colors = [LABEL_COLOR_MAP[l] for l in labels]
plt.scatter(X[:, 0], X[:, 1], c=label_colors)

"""















