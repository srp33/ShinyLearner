from sklearn.preprocessing import *
import pandas as pd
from sys import argv

file_path = argv[1]
verbose = argv[2] == "true"
scaler = argv[3]

#####################################################################################
# Scaler Options
# (https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html)
# standard = StandardScaler
# minmax = MinMaxScaler
# maxabs = MaxAbsScaler
# power = PowerTransformer
# quantnorm = QuantileTransformer w/ normal output
# quantunif = QuantileTransformer w/ uniform output
# normalizer = Normalizer
# robust = RobustScaler
#####################################################################################

def scale_data(file_path, scaler, verbose):
    scaler = scaler.lower()
    data = pd.read_csv(file_path, sep='\t', index_col=0)
    index = data.index

    # Ignore columns that don't contain numerical values
    non_num_columns = []
    dtypes = data.columns.to_series().groupby(data.dtypes).groups
    dtypes = {k.name: list(v) for k, v in dtypes.items()}

    for dtype in dtypes.keys():
        if 'float' not in dtype and 'int' not in dtype:
            non_num_columns += dtypes[dtype]

    if verbose and len(non_num_columns) > 0:
        print('The following columns do not contain numerical values and will not be scaled:')
        print('\t', ', '.join(sorted(list(set(non_num_columns)))))

    # Add the class column, which should never be scaled
    if "Class" in data:
        non_num_columns.append('Class')

#    # Ignore columns that contain numbers, but where fewer than half are distinct values
#    categorical_columns = []
#    num_unique = data.columns.to_series().groupby(data.nunique()).groups
#    num_unique = {k: list(v) for k, v in num_unique.items()}
#
#    for num in num_unique.keys():
#        if num < len(index) * 0.5:
#            categorical_columns += num_unique[num]
#    if verbose and len(categorical_columns) > 0:
#        print('In the following columns, fewer than half are distinct values, so they will not be scaled:')
#        print('\t', ', '.join(categorical_columns))
#
#    excluded_columns = list(set(non_num_columns + categorical_columns))
    excluded_data = data[non_num_columns]

    scaled_data = data.drop(non_num_columns, axis=1)
    scaled_columns = scaled_data.columns

    if len(scaled_columns) > 0:
        if scaler == 'standard':
            if verbose:
                print("Applying the standard scaler (mean of zero, unit variance)")
            transformer = StandardScaler()
        elif scaler == 'minmax':
            if verbose:
                print("Applying the min-max scaler")
            transformer = MinMaxScaler()
        elif scaler == 'maxabs':
            if verbose:
                print("Applying the max absolute scaler")
            transformer = MaxAbsScaler()
        elif scaler == 'power':
            if verbose:
                print("Applying the power transformer for scaling")
            transformer = PowerTransformer()
        elif scaler == 'quantnorm':
            if verbose:
                print('Quantile scaling to the normal (Gaussian) distribution')
            transformer = QuantileTransformer(output_distribution='normal')
        elif scaler == 'quantunif':
            if verbose:
                print('Quantile scaling to the uniform distribution')
            transformer = QuantileTransformer(output_distribution='uniform')
        elif scaler == 'normalizer':
            if verbose:
                print('Scaling using the normalizer approach')
            transformer = Normalizer()
        else:
            if verbose:
                print('Scaling using the robust approach')
            transformer = RobustScaler()

        scaled_data = transformer.fit_transform(scaled_data)
        scaled_data = pd.DataFrame(scaled_data, index=index, columns=scaled_columns)
        data = pd.concat([scaled_data, excluded_data], axis=1, join='inner')
        if verbose:
            print('Saving scaled version of data to {}'.format(file_path))

        data.to_csv(file_path, index_label='', sep='\t', compression="gzip")
    else:
        if verbose:
            print('No columns to be scaled, no action was performed')

scale_data(file_path, scaler, verbose)
