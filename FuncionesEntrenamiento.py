from sklearn.metrics import roc_curve
import numpy as np
import pandas as pd
import tensorflow as tf
from threading import Thread

'''
Class prepared by the student Manuel Méndez Calvo, computer engineering student at UVa. The objective of this class is
to be part of the TFG on the creation of classifiers for neural networks with data visualization.

This function is a helper for the execution of neural networks. In it we will have the different functions that we will
be invoking throughout the execution and that will allow us to make everything work correctly.
'''

'''
This function aims to expand the architecture described by the dictionary, iterating through attributes and
generating a list with the expanded architecture.
'''
def ExpandDict( Grid):

    Expand = [Grid]

    atribList = Grid.keys()

    # We expand for each attribute, starting from what was expanded before

    for atribExpand in atribList:
        # For each expanded item we repeat it for the next attribute, saving the new ones in a list
        itemsNuevosList = []

        for itemExpand in Expand:
            # We expand by the selected attribute
            valor = itemExpand[atribExpand]
            valorList = valor.split(sep=",")
            if len(valorList) > 1:
                for valor in valorList:
                    itemNuevo = itemExpand.copy()
                    itemNuevo[atribExpand] = valor

                    itemsNuevosList.append(itemNuevo)
            else:
                # The element had nothing to expand on that attribute, so it goes into the list as-is.

                itemsNuevosList.append(itemExpand)

        Expand = itemsNuevosList

    return Expand

'''
Function intended to split a multivariate sequence into samples
'''
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


'''
Function for calculating the error
'''
def CalculaEER( Estimado, Real):
    fpr, tpr, threshold = roc_curve(Real, Estimado, pos_label=1)
    fnr = 1 - tpr
    eer_threshold = threshold[np.nanargmin(np.absolute((fnr - fpr)))]
    EER = fpr[np.nanargmin(np.absolute((fnr - fpr)))]

    return EER

'''
This function is intended to make a thread of iterations where we can parallelize the different calculations of
the execution, making it much faster
'''
def HiloIteracion(pathModelo, X_train, y_train, X_test, y_test, ResultadosQ, loss, optimizer, epocas):

    modelo = tf.keras.models.load_model(pathModelo)
    modelo.compile(loss=loss, optimizer=optimizer, metrics=['accuracy'])
    modelo.fit(X_train, y_train, batch_size=64, epochs=epocas, verbose=0)

    Salida_red = modelo.predict(X_test)
    Salida_red = Salida_red.reshape(-1, 1)


    EERhilo = CalculaEER(Salida_red, y_test.reshape(-1, 1))

    ResultadosQ.put(EERhilo)


'''
Function intended to generate user data based on the given input
'''
def GenDataUsr(DatosDF, usuario, marca, sensor):

    # To train:

    # Authentic:

    # - From the TFM set. of the mark, the sample 1 of the session 1 of the user --> Exit 1 (correct)
    Entren1 = DatosDF.loc[(DatosDF.Conjunto == "TFM") &
                          (DatosDF.Marca == marca) &
                          (DatosDF.NombreUsr == usuario) &
                          (DatosDF.Sensor == sensor) &
                          (DatosDF.Sesion == 1) &
                          (DatosDF.Muestra == 1)]
    Entren1["Salida"] = 1.0

    # Impostor:
    # - All the samples of the TFG set --> Output 0 (imposters)
    Entren0 = DatosDF.loc[(DatosDF.Conjunto == "TFG") &
                          (DatosDF.Marca == marca) &
                          (DatosDF.Sensor == sensor)]
    Entren0["Salida"] = 0.0

    Entren = Entren0

    Entren = pd.concat([Entren, Entren1], ignore_index=True)
    Entren.drop(Entren.columns[3:11], axis=1, inplace=True)

    # Test

    # Authentic
    # - Samples 1 and 2 of session 2 --> Output 1 (correct)
    Prueba1 = DatosDF.loc[(DatosDF.Conjunto == "TFM") &
                          (DatosDF.NombreUsr == usuario) &
                          (DatosDF.Marca == marca) &
                          (DatosDF.Sensor == sensor) &
                          (DatosDF.Sesion == 2) & ((DatosDF.Muestra == 1) | (DatosDF.Muestra == 2))]
    Prueba1["Salida"] = 1.0

    # Impostor:
    # - The unused TFM samples of impostors (sample!=1 or session != 1) --> Output 0 (impostor)
    Prueba0 = DatosDF.loc[(DatosDF.Conjunto == "TFM") &
                          (DatosDF.Marca == marca) &
                          (DatosDF.NombreUsr != usuario) &
                          ((DatosDF.Sesion != 1) | (DatosDF.Muestra != 1))]
    Prueba0["Salida"] = 0.0

    Prueba = Prueba0
    Prueba = pd.concat([Prueba, Prueba1], ignore_index=True)
    Prueba.drop(Prueba.columns[3:11], axis=1, inplace=True)

    return Entren, Prueba

'''
Function intended for training and testing. For this, the number of repetitions by default is 5
'''
def EntrenaYPrueba(pathModelo, usuario, listaMar, listaSen, TodoDF, tipo, ResultadosQ, loss, optimizer, epocas, log):
    # Repetitions is the number of times the training/test is repeated. 5 default

    Resultados = pd.DataFrame(columns=("Usuario", "Marca", "Sensor", "Score", "EER"))

    for marca in listaMar:
        ### Sensor (GYR o ACC)
        for sensor in listaSen:
            # We only create models for users of the TFM set
            if usuario.startswith("TFG"):
                continue

            Entren, Prueba = GenDataUsr(TodoDF, usuario, marca, sensor)
            log.append('<font size="4"><u>'
                                  'Datos Generados para usuario: '+ usuario + ' ' + marca +' ' + sensor + ''
                                  '</u></font size="4">')

            X_train, y_train = split_sequences(np.array(Entren), 80)
            X_test, y_test = split_sequences(np.array(Prueba), 80)
            # # If the first layer is "Dense", as is the case in this version, the tensor
            # generated by split_sequences must be adapted:
            if tipo == 'Dense':
                # We are going to put in each entry a window of 80 samples, each sample with 3 data-dimensions.
                # That is, the inputs are vectors of 3x80=240 components.
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
                # We wait for the threads to finish
                Hilo.join()

            # The score column is set to -1 by default because it is only good for binary classifications
            Resultados.loc[len(Resultados)] = {"Usuario": usuario,
                                               "Marca": marca, "Sensor": sensor,
                                               "Score": -1.0,
                                               "EER": ' '.join(map(str, EER))}
    return Resultados


