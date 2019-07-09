from sys import argv
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from tensorflow import ConfigProto, Session
from tensorflow.keras import backend as K
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dropout, Dense, Input, Add, Activation, AlphaDropout
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

LAYER_WIDTH = int(ALGORITHM_ARGS[0])
NUM_LAYERS = int(ALGORITHM_ARGS[1])
DROPOUT_RATE = float(ALGORITHM_ARGS[2])
REGULARIZATION = float(ALGORITHM_ARGS[3])
ACTIVATION = ALGORITHM_ARGS[4]
LEARNING_RATE = float(ALGORITHM_ARGS[5])
EPOCHS = int(ALGORITHM_ARGS[6])
# KEY_FILE = ALGORITHM_ARGS[7]

train_df = pd.read_csv(TRAIN_FILE, sep='\t', index_col=0)
x_train = train_df.drop('Class', axis=1).values
y_train = np.array([CLASS_OPTIONS.index(str(y[0])) for y in train_df.loc[:, ["Class"]].values.tolist()])
y_train = y_train.reshape(-1, 1)
y_train = OneHotEncoder(categories='auto').fit_transform(y_train).toarray()

x_test = pd.read_csv(TEST_FILE, sep='\t', index_col=0)
# y_test = pd.read_csv(KEY_FILE, sep='\t', index_col=0)
# y_test = np.array([CLASS_OPTIONS.index(str(y[0])) for y in y_test.loc[:, ["Class"]].values.tolist()])
# y_test = y_test.reshape(-1, 1)
# y_test = OneHotEncoder().fit_transform(y_test).toarray()


def gpu_setup():
    cfg = ConfigProto()
    cfg.gpu_options.allow_growth = True
    K.set_session(Session(config=cfg))


def resnet(x, y, test):
    dropout = AlphaDropout if ACTIVATION == 'snn' else Dropout
    n_inputs = x.shape[1]
    n_outputs = y.shape[1]
    input_layer = Input(shape=(n_inputs,), name='input')
    input = Dense(LAYER_WIDTH,
                  kernel_regularizer=l2(REGULARIZATION),
                  kernel_initializer='lecun_normal',
                  bias_initializer='zeros',
                  activation=ACTIVATION,
                  name='reinjected_input')(input_layer)
    layer = None
    for i in range(NUM_LAYERS):
        layer = Dense(LAYER_WIDTH,
                      kernel_regularizer=l2(REGULARIZATION),
                      kernel_initializer='lecun_normal',
                      bias_initializer='zeros',
                      activation=ACTIVATION,
                      name='dense{}_1'.format(i + 1))(input if i == 0 else layer)
        layer = dropout(DROPOUT_RATE, name='dropout{}_1'.format(i + 1))(layer)
        layer = Dense(LAYER_WIDTH,
                      kernel_regularizer=l2(REGULARIZATION),
                      kernel_initializer='lecun_normal',
                      bias_initializer='zeros',
                      name='dense{}_2'.format(i + 1))(layer)
        layer = Add(name='reinjection_{}'.format(i + 1))([input, layer])
        layer = Activation(ACTIVATION, name='block_activation_{}'.format(i + 1))(layer)
        layer = dropout(DROPOUT_RATE, name='dropout{}_2'.format(i + 1))(layer)
    logits = Dense(n_outputs,
                   kernel_initializer='lecun_normal',
                   bias_initializer='zeros',
                   name='logits')(layer)
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
    model.compile(optimizer=Adam(LEARNING_RATE), loss=loss)
    model.fit(x, y, verbose=0, epochs=EPOCHS, batch_size=200)
    predictions = model.predict(test, verbose=False)
    for prediction in predictions:
        probs = [str(prob) for prob in list(prediction)]
        print('{}\t{}'.format(CLASS_OPTIONS[np.argmax(prediction)], '\t'.join(probs)))

resnet(x_train, y_train, x_test)
