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
    data = pd.read_csv(file_path, sep='\t', index_col=0)
    index = data.index

    # Remove columns that don't contain numerical values
    non_num_columns = ['Class']
    dtypes = data.columns.to_series().groupby(data.dtypes).groups
    dtypes = {k.name: list(v) for k, v in dtypes.items()}
    for dtype in dtypes.keys():
        if 'float' not in dtype and 'int' not in dtype:
            non_num_columns += dtypes[dtype]
    if verbose:
        print('The following columns do not contain numerical values and will not be scaled:')
        print('\t', ', '.join(set(non_num_columns)))

    # Remove columns that contain numbers, but fewer than half are distinct values
    categorical_columns = []
    num_unique = data.columns.to_series().groupby(data.nunique()).groups
    num_unique = {k: list(v) for k, v in num_unique.items()}
    for num in num_unique.keys():
        if num < len(index) * 0.5:
            categorical_columns += num_unique[num]
    if verbose and len(categorical_columns) > 0:
        print('In the following columns, fewer than half are distinct values, so they will not be scaled:')
        print('\t', ', '.join(categorical_columns))

    excluded_columns = set(non_num_columns + categorical_columns)
    excluded_data = data[excluded_columns]
    scaled_data = data.drop(excluded_columns, axis=1)
    scaled_columns = scaled_data.columns
    if len(scaled_columns) > 0:
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
            print('Using scaler of class "{}" to scale data'.format(str(type(transformer)).split("'")[1]))
        scaled_data = transformer.fit_transform(scaled_data)
        scaled_data = pd.DataFrame(scaled_data, index=index, columns=scaled_columns)
        data = pd.concat([scaled_data, excluded_data], axis=1, join='inner')
        if verbose:
            print('Saving scaled version of data to {}'.format(file_path))
        data.to_csv(file_path, index_label='', sep='\t')
    else:
        if verbose:
            print('No columns remain to be scaled, no action was performed')

scale_data(file_path, scaler, verbose)
