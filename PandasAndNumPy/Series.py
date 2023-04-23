#https://www.javatpoint.com/python-pandas-series

# creatign empty series
import pandas as pd
x = pd.Series()
print (x)


# creating using the the array
import numpy as np
import pandas as pd

data=np.array(['p','y','t','h','o','n'])
series1=pd.Series(data,index=[6,2,2,3,4,3])
print(series1)

# Creating using the dic
import pandas as pd
import numpy as np
info = {'x' : 0., 'y' : 1., 'z' : 2.}
a = pd.Series(info,index=['x',2,3])
print (a)

#Create a Series using Scalar:

s=pd.Series(4,index=[1,2,3,4])
print(s)

#Accessing data from series with Position:
import pandas as pd
import numpy as np
data=np.array(['p','y','t','h','o','n'])
series1=pd.Series(data,index=[6,2,2,3,4,3])
# get acccess the index lable
print(series1[6])


#Series object attributes
import pandas as pd
import numpy as np
data=np.array(['p','y','t','h','o','NaN'])
series1=pd.Series(data,index=[6,2,2,3,3,5])
# get acccess the index lable
print(series1.index)
print(series1.shape)
print(series1.dtype)
print(series1.size)
print(series1.empty)
print(series1.hasnans)
print(series1.nbytes)
print(series1.ndim)
print(series1.itemsize)



# Series.map() Map the values from two series that have a common column.
import pandas as pd
import numpy as np
a = pd.Series(['Java', 'C', 'C++', np.nan])
print(a.map({'Java': 'Core'}))
print(a.map('I like {}'.format, na_action='ignore'))

#standar deviation.
import pandas as pd
# calculate standard deviation
import numpy as np
print(np.std([4,7,2,1,6,3]))
print(np.std([6,9,15,2,-17,15,4]))

#series to frame.
import pandas as pd
s=pd.Series(['p','y','t','h','o','n'], name='values')
print(s)
print(s.to_frame())


import pandas as pd
import matplotlib.pyplot as plt
emp = ['Parker', 'John', 'Smith', 'William']
id = [102, 107, 109, 114]
emp_series = pd.Series(emp)
id_series = pd.Series(id)
frame = { 'Emp': emp_series, 'ID': id_series }
result = pd.DataFrame(frame)
print(result)

#series to unique.
import pandas as pd
pd.unique(pd.Series([2, 1, 3, 3]))
print(pd.unique(pd.Series([pd.Timestamp('20160101'),pd.Timestamp('20160101')])))

import pandas as pd
print(pd.unique(pd.Series([2, 1, 3, 3])))

# series value counts

import pandas as pd
import numpy as np
index = pd.Index([2, 1, 1, np.nan, 3])
print(index)
print(index.value_counts())

import pandas as pd
index = pd.Index([1, 3, 2, 2, 1, np.nan])
index.value_counts()
a = pd.Series([1, 3, 2, 2, 1, np.nan])
print(a.value_counts(dropna=False))


import numpy as np

print(np.arrange(10))



# import pandas as pd
#
# # a simple list
# list = ['g', 'e', 'e', 'k', 's']
# # create series form a list
# ser = pd.Series(list)
# print(ser)
#
# import pandas as pd
#
# # giving a scalar value with index
# ser = pd.Series(10, index=[0, 1, 2, 3, 4, 5])
#
# print(ser)
#
