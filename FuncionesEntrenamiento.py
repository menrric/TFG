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
from threading import Thread, Lock
from queue import Queue
import xml.etree.ElementTree as ET
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

    return EER


def HiloIteracion(pathModelo, X_train, y_train, X_test, y_test, ResultadosQ, loss, optimizer, epocas):

    modelo = tf.keras.models.load_model(pathModelo)
    modelo.compile(loss=loss, optimizer=optimizer, metrics=['accuracy'])
    modelo.fit(X_train, y_train, batch_size=64, epochs=epocas, verbose=0)

    Salida_red = modelo.predict(X_test)
    Salida_red = Salida_red.reshape(-1, 1)

    # Evaluamos

    EERhilo = CalculaEER(Salida_red, y_test.reshape(-1, 1))

    # MutexHilos.release()
    ResultadosQ.put(EERhilo)


# Entrena y prueba para sólo un usuario. Retorna EER para ese usuario.
# Asume ya definidas ListaMar y ListaSen

def GenDataUsr(DatosDF, usuario, marca, sensor):  # El conjunto está implícito en la variable usuario

    # Para Entrenar:

    # Auténticos:

    # Muestras de entrenamiento:
    # - Del conjunto TFM. de la marca, la muestra 1 de la sesión 1 del usuario --> Salida 1 (correcto)
    Entren1 = DatosDF.loc[(DatosDF.Conjunto == "TFM") &
                          (DatosDF.Marca == marca) &
                          (DatosDF.NombreUsr == usuario) &
                          (DatosDF.Sensor == sensor) &
                          (DatosDF.Sesion == 1) &
                          (DatosDF.Muestra == 1)]
    Entren1["Salida"] = 1.0

    # El conjunto de impostores para entrenar
    # - Todas las muestras del conjunto TFG --> Salida 0 (impostores)
    Entren0 = DatosDF.loc[(DatosDF.Conjunto == "TFG") &
                          (DatosDF.Marca == marca) &
                          (DatosDF.Sensor == sensor)]
    Entren0["Salida"] = 0.0

    Entren = Entren0

    Entren = pd.concat([Entren, Entren1], ignore_index=True)
    Entren.drop(Entren.columns[3:11], axis=1, inplace=True)

    # Para probar

    # Auténticas
    # - Muestras 1 y 2 de la sesión 2 --> Salida 1 (correcto)
    Prueba1 = DatosDF.loc[(DatosDF.Conjunto == "TFM") &
                          (DatosDF.NombreUsr == usuario) &
                          (DatosDF.Marca == marca) &
                          (DatosDF.Sensor == sensor) &
                          (DatosDF.Sesion == 2) & ((DatosDF.Muestra == 1) | (DatosDF.Muestra == 2))]
    Prueba1["Salida"] = 1.0

    # Impostores:
    # - Las muestras de TFM no usadas de impostores (muestra!=1 o sesión != 1) --> Salida 0 (impostor)
    Prueba0 = DatosDF.loc[(DatosDF.Conjunto == "TFM") &
                          (DatosDF.Marca == marca) &
                          (DatosDF.NombreUsr != usuario) &
                          ((DatosDF.Sesion != 1) | (DatosDF.Muestra != 1))]
    Prueba0["Salida"] = 0.0

    Prueba = Prueba0
    Prueba = pd.concat([Prueba, Prueba1], ignore_index=True)
    Prueba.drop(Prueba.columns[3:11], axis=1, inplace=True)

    return Entren, Prueba

def EntrenaYPrueba(pathModelo, usuario, listaMar, listaSen, TodoDF, tipo, ResultadosQ, loss, optimizer, epocas, log):
    # Repeticiones es el número de veces que se repite
    # el entrenamiento/prueba.

    Resultados = pd.DataFrame(columns=("Usuario", "Marca", "Sensor", "Score", "EER"))

    for marca in listaMar:
        ### Por sensor (GYR o ACC)
        for sensor in listaSen:
            # Sólo creamos modelos para usuarios del conjunto TFM
            if usuario.startswith("TFG"):
                continue

            Entren, Prueba = GenDataUsr(TodoDF, usuario, marca, sensor)
            log.append('<font size="4"><u>'
                                  'Datos Generados para usuario: '+ usuario + marca + sensor +''
                                  '</u></font size="4">')


            # Adaptamos los datos para la red CNN

            # Como en los experimentos previos se usó una ventana de 8 segundos,
            # ahora vamos a crear secuencias de 80 muestras (a 0.1 segundos por muestra)

            X_train, y_train = split_sequences(np.array(Entren), 80)
            X_test, y_test = split_sequences(np.array(Prueba), 80)
            # Si la primera capa es "Dense" (probablemente porque estemos usando
            # un MLP), hay que adaptar el tensor generado por split_sequences:
            if tipo == 'Dense':
                # Vamos a poner en cada entrada una ventana de 80 muestras,
                # cada muestra con 3 datos-dimensiones.
                # Es decir, las entradas son vectores de 3x80=240 componentes.
                X_train = X_train.reshape(-1, 80 * 3)
                X_test = X_test.reshape(-1, 80 * 3)

            ListaHilos = []
            EER = []

            for repeticion in range(0, 5):
                Hilo = Thread(target=HiloIteracion,
                              args=(pathModelo, X_train, y_train, X_test, y_test, ResultadosQ, loss, optimizer, epocas))

                ListaHilos.append(Hilo)
                Hilo.start()

            for Hilo in ListaHilos:
                ret = ResultadosQ.get()
                EER.append(ret)

            for Hilo in ListaHilos:
                # Esperamos a que terminen los hilos
                Hilo.join()

            # La columna Score la pongo a -1.0, porque no se usa (sólo tiene sentido cuando
            # se hace una clasificaicón con etiqueta binaria True/False)
            Resultados.loc[len(Resultados)] = {"Usuario": usuario,
                                               "Marca": marca, "Sensor": sensor,
                                               "Score": -1.0,
                                               "EER": ' '.join(map(str, EER))}
    return Resultados


