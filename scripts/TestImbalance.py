
# coding: utf-8

# # Read it in

# In[26]:




# In[93]:




# # Get subset as numpy arrays

# In[ ]:




# In[ ]:




# #### X and y get change in a function, then we write them

# In[ ]:




# In[ ]:




# In[ ]:




# In[19]:

import pandas as pd
import numpy as np
import sys

#DataFilePath = sys.argv[1]
#Prefix = sys.argv[2]
#OutFilePath = sys.argv[3]

DataFilePath = "StrongSignal_Continuous.tsv.gz"

#add checks to make sure command line data is valid

df = pd.read_csv(DataFilePath, sep = '\t', index_col = 0)


X = df.iloc[:,:-1].values.astype(np.float32)
X_columns = df.iloc[:,:-1].columns

y = df.iloc[:,-1:].values.astype(np.int32).ravel()
y_columns = df.iloc[:,-1:].columns

#from imblearn.under_sampling import NearMiss
#from imblearn.under_sampling import ClusterCentroids
#from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import ADASYN



#sampler = NearMiss(version=2)
#sampler = ClusterCentroids()
#sampler = RandomOverSampler()
sampler = ADASYN()

X_resampled, y_resampled = sampler.fit_sample(X, y)

X_Final = pd.DataFrame(data=X_resampled,columns=X_columns)
y_Final = pd.DataFrame(data=y_resampled,columns=y_columns)

X_y_Final = pd.concat([X_Final,y_Final], axis=1)

X_y_Final.to_csv('output_X.tsv', sep='\t')
print X_y_Final


# In[2]:

print type(X_y_Final)


# In[ ]:



