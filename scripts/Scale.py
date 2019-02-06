from sklearn.preprocessing import *
import pandas as pd
from sys import argv


file_path = argv[7]
verbose = argv[8] == "true"
scaler = argv[9]


#####################################################################################
# Scaler Options
# (https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html)
# Standard = StandardScaler
# Robust = RobustScaler
# MinMax = MinMaxScaler
# MaxAbs = MaxAbsScaler
# Power = PowerTransformer
# QuantileNormal = QuantileTransformer w/ normal output
# QuantileUniform = QuantileTransformer w/ uniform output
# Normalizer = Normalizer
#####################################################################################


def scale_data(file_path, scaler='robust', verbose=False):
    scaler = scaler.lower()
    gzip = False
    if file_path.endswith('.gz'):
        gzip = True
    data = pd.read_csv(file_path, sep='\t', index_col=0)
    index = data.index
    x = data.drop('Class', axis=1)
    x_columns = x.columns
    y = data[['Class']]
    if scaler == 'standard':
        transformer = StandardScaler()
    elif scaler == 'minmax':
        transformer = MinMaxScaler()
    elif scaler == 'maxabs':
        transformer = MaxAbsScaler()
    elif 'power' in scaler:
        transformer = PowerTransformer()
    elif 'quantile' in scaler:
        if 'normal' in scaler:
            if verbose:
                print('Outputting normal (Gaussian) distribution')
            transformer = QuantileTransformer(output_distribution='normal')
        else:
            transformer = QuantileTransformer(output_distribution='uniform')
            if verbose:
                print('Outputting uniform distribution')
    elif scaler == 'normalizer':
        transformer = Normalizer()
    else:
        transformer = RobustScaler()
    if verbose:
        print('Using scaler of class "{}"'.format(str(type(transformer)).split("'")[1]))
    x = transformer.fit_transform(x)
    x = pd.DataFrame(x, index=index, columns=x_columns)
    data = pd.concat([x, y], axis=1, join='inner')
    data.to_csv(file_path, index_label='', sep='\t', compression='gzip' if gzip else None)


scale_data(file_path, scaler, verbose)
