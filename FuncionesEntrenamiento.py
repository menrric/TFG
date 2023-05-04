import errno

from keras import Sequential
from keras.layers import Dense

from sklearn.metrics import roc_curve
import copy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
import os
def ExpandDict( Grid):
    # Vamos a expandir la arquitectura descrita por el diccionario Grid yendo
    # atributo (clave) por atributo, y generando una lista de arquitecturas
    # expandidas.

    # Expand va a ser una lista de diccionarios (arquitecturas) a expandir.
    # El primer item
    Expand = [Grid]

    # Creamos una lista de atributos:
    atribList = Grid.keys()

    # Expandimos por cada atributo, partiendo de lo expandido antes

    for atribExpand in atribList:
        # Para cada item expandido lo repetimos para el siguiente atributo

        # Guardamos los nuevos items expandidos en una lista
        itemsNuevosList = []

        for itemExpand in Expand:
            # Expandimos por el atributo seleccionado
            valor = itemExpand[atribExpand]
            valorList = valor.split(sep=",")
            if len(valorList) > 1:
                # Hay algo que expandir...
                for valor in valorList:
                    itemNuevo = itemExpand.copy()  # Creamos una copia por cada valor
                    itemNuevo[atribExpand] = valor

                    itemsNuevosList.append(itemNuevo)
            else:
                # El elemento no tenía nada que expandir en ese atributo,
                # por lo que pasa a la lista tal cual.

                itemsNuevosList.append(itemExpand)

        Expand = itemsNuevosList

    return Expand


# split a multivariate sequence into samples
def split_sequences( sequences, n_steps):
    X, y = list(), list()
    for i in range(len(sequences)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the dataset
        if end_ix > len(sequences):
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix - 1, -1]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)


# Cálculo del Equi Error

def CalculaEER( Estimado, Real):
    fpr, tpr, threshold = roc_curve(Real, Estimado, pos_label=1)
    fnr = 1 - tpr
    eer_threshold = threshold[np.nanargmin(np.absolute((fnr - fpr)))]
    EER = fpr[np.nanargmin(np.absolute((fnr - fpr)))]
    # print ("EER=",EER)

    return EER
