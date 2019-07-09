from sys import argv
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from tensorflow import ConfigProto, Session
from tensorflow.keras import backend as K
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dropout, Dense, Input, Flatten, BatchNormalization, Activation, AlphaDropout
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import binary_crossentropy, categorical_crossentropy
from tensorflow.keras.utils import multi_gpu_model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'

TRAIN_FILE = argv[1]
TEST_FILE = argv[2]
CLASS_OPTIONS = argv[3].split(',')
NUM_CORES = argv[4]
VERBOSE = argv[5] == 'true'

ALGORITHM_ARGS = argv[6].split(";")

MODEL_TYPE = ALGORITHM_ARGS[0]
LAYERS = ALGORITHM_ARGS[1].split(',')
DROPOUT_RATE = float(ALGORITHM_ARGS[2])
REGULARIZATION_RATE = float(ALGORITHM_ARGS[3])
BATCH_NORMALIZATION = (MODEL_TYPE != 'snn' and ALGORITHM_ARGS[4] == 'true')
EPOCHS = int(ALGORITHM_ARGS[5])

train_df = pd.read_csv(TRAIN_FILE, sep='\t', index_col=0)
x_train = train_df.drop('Class', axis=1).values
y_train = np.array([CLASS_OPTIONS.index(str(y[0])) for y in train_df.loc[:, ["Class"]].values.tolist()])
y_train = y_train.reshape(-1, 1)
y_train = OneHotEncoder(categories="auto").fit_transform(y_train).toarray()

x_test = pd.read_csv(TEST_FILE, sep='\t', index_col=0)


def gpu_setup():
    cfg = ConfigProto()
    cfg.gpu_options.allow_growth = True
    K.set_session(Session(config=cfg))


def dnn(x, y, test):
    activation = 'selu' if MODEL_TYPE == 'snn' else 'elu'
    dropout = AlphaDropout if MODEL_TYPE == 'snn' else Dropout
    layers = []
    for layer in LAYERS:
        if int(layer) > 0:
            layers.append(int(layer))
    n_inputs = x.shape[1]
    n_outputs = y.shape[1]
    input_layer = Input(shape=(n_inputs,), name='input')
    layer = Flatten()(input_layer)
    if DROPOUT_RATE > 0:
        layer = dropout(DROPOUT_RATE, name='dropout_input')(layer)
    for i in range(len(layers)):
        layer = Dense(layers[i],
                      kernel_regularizer=l2(REGULARIZATION_RATE),
                      activation=activation,
                      name='dense_{}'.format(i + 1))(layer)
        if BATCH_NORMALIZATION:
            layer = BatchNormalization(name='batch_norm_{}'.format(i + 1))(layer)
        if DROPOUT_RATE > 0:
            layer = dropout(DROPOUT_RATE, name='dropout_{}'.format(i + 1))(layer)
    logits = Dense(n_outputs, name='logits')(layer)
    probabilities = Activation('softmax', name='output')(logits)
    if n_outputs == 2:
        loss = binary_crossentropy
    else:
        loss = categorical_crossentropy
    model = Model(input_layer, probabilities)
    try:
        gpu_setup()
        model = multi_gpu_model(model, gpus=2)
    except:
        pass
    model.compile(optimizer=Adam(), loss=loss)
    model.fit(x, y, verbose=0, epochs=EPOCHS, batch_size=200)
    #predictions = model.predict(test, verbose=VERBOSE)
    predictions = model.predict(test, verbose=False)
    for prediction in predictions:
        probs = [str(prob) for prob in list(prediction)]
        print('{}\t{}'.format(CLASS_OPTIONS[np.argmax(prediction)], '\t'.join(probs)))


dnn(x_train, y_train, x_test)
