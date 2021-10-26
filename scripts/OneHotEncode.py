import sys
import pandas
import numpy as np

inFilePath = sys.argv[1]

data = pandas.read_csv(inFilePath, index_col=0, sep="\t")

colsToEncode = [x for x in data.columns if data[x].dtype != np.float64 and data[x].dtype != np.int64 and x != "Class"]

if len(colsToEncode) > 0:
    data = pandas.get_dummies(data, drop_first=True, columns=colsToEncode)
    data.to_csv(inFilePath, sep="\t", compression="gzip")
