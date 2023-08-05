# dataframe_column_identifier
## `latest version: 0.0.3`

## What is this?
A light and useful package to find columns in a Dataframe by its values.

## Installing
```
pip install dataframe-column-identifier==0.0.3
```

## Importing
```
from dataframe_column_identifier import DataFrameColumnIdentifier
```

## KBest - Feature Selection Using Example
```
import pandas as pd
from sklearn.feature_selection import SelectKBest, mutual_info_regression
from dataframe_column_identifier import DataFrameColumnIdentifier

print(X_train.shape)
(1460, 282)

print(X_test.shape)
(1459, 282)

dfci = DataFrameColumnIdentifier()
kbest = SelectKBest(score_func=mutual_info_regression, k=10)
kbest.fit_transform(X_train, y_train)
kbest_get_support_output = kbest.get_support()

print(kbest_get_support_output)
array([False,  True, False,  True, False,  True, False,  True,  True,
       False, False,  True, False, False, False, False, False, False,
        True,  True,  True, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False,  True, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False, False, False, False, False, False, False,
       False, False, False])

print(dfci.select_columns_KBest(X_train, kbest_get_support_output, verbose=1))
[
  '1stFlrSF',
  'ExterQual_TA',
  'GarageArea',
  'GarageCars',
  'GarageYrBlt',
  'GrLivArea',
  'MSSubClass',
  'OverallQual',
  'TotalBsmtSF',
  'YearBuilt'
]

X_train = dfci.transform(X_train)
X_test = dfci.transform(X_test)

print(X_train.shape)
(1460, 10)

print(X_test.shape)
(1459, 10)

print(X_train.head(10))
   1stFlrSF  ExterQual_TA  GarageArea  GarageCars  GarageYrBlt  GrLivArea  MSSubClass  OverallQual  TotalBsmtSF  YearBuilt
0     856.0           0.0       548.0         2.0       2003.0     1710.0        60.0          7.0        856.0     2003.0
1    1262.0           1.0       460.0         2.0       1976.0     1262.0        20.0          6.0       1262.0     1976.0
2     920.0           0.0       608.0         2.0       2001.0     1786.0        60.0          7.0        920.0     2001.0
3     961.0           1.0       642.0         3.0       1998.0     1717.0        70.0          7.0        756.0     1915.0
4    1145.0           0.0       836.0         3.0       2000.0     2198.0        60.0          8.0       1145.0     2000.0
5     796.0           1.0       480.0         2.0       1993.0     1362.0        50.0          5.0        796.0     1993.0
6    1694.0           0.0       636.0         2.0       2004.0     1694.0        20.0          8.0       1686.0     2004.0
7    1107.0           1.0       484.0         2.0       1973.0     2090.0        60.0          7.0       1107.0     1973.0
8    1022.0           1.0       468.0         2.0       1931.0     1774.0        50.0          7.0        952.0     1931.0
9    1077.0           1.0       205.0         1.0       1939.0     1077.0       190.0          5.0        991.0     1939.0

print(X_test.head(10))
   1stFlrSF  ExterQual_TA  GarageArea  GarageCars  GarageYrBlt  GrLivArea  MSSubClass  OverallQual  TotalBsmtSF  YearBuilt
0     896.0           1.0       730.0         1.0       1961.0      896.0        20.0          5.0        882.0     1961.0
1    1329.0           1.0       312.0         1.0       1958.0     1329.0        20.0          6.0       1329.0     1958.0
2     928.0           1.0       482.0         2.0       1997.0     1629.0        60.0          5.0        928.0     1997.0
3     926.0           1.0       470.0         2.0       1998.0     1604.0        60.0          6.0        926.0     1998.0
4    1280.0           0.0       506.0         2.0       1992.0     1280.0       120.0          8.0       1280.0     1992.0
5     763.0           1.0       440.0         2.0       1993.0     1655.0        60.0          6.0        763.0     1993.0
6    1187.0           1.0       420.0         2.0       1992.0     1187.0        20.0          6.0       1168.0     1992.0
7     789.0           1.0       393.0         2.0       1998.0     1465.0        60.0          6.0        789.0     1998.0
8    1341.0           1.0       506.0         2.0       1990.0     1341.0        20.0          7.0       1300.0     1990.0
9     882.0           1.0       525.0         2.0       1970.0      882.0        20.0          4.0        882.0     1970.0
```

## Feature Selection Using Example
```
import pandas as pd
from sklearn.feature_selection import SelectKBest, mutual_info_regression
from dataframe_column_identifier import DataFrameColumnIdentifier

print(X_train.shape)
(1460, 282)

print(X_test.shape)
(1459, 282)

dfci = DataFrameColumnIdentifier()
kbest = SelectKBest(score_func=mutual_info_regression, k=10)
kbest_selected_features = kbest.fit_transform(X_train, y_train)

print(kbest_selected_features.shape)
(1460, 10)

print(pd.DataFrame(kbest_selected_features).head(10))
        0    1       2       3       4       5       6    7      8    9
 0   60.0  7.0  2003.0   856.0   856.0  1710.0  2003.0  2.0  548.0  0.0
 1   20.0  6.0  1976.0  1262.0  1262.0  1262.0  1976.0  2.0  460.0  1.0
 2   60.0  7.0  2001.0   920.0   920.0  1786.0  2001.0  2.0  608.0  0.0
 3   70.0  7.0  1915.0   756.0   961.0  1717.0  1998.0  3.0  642.0  1.0
 4   60.0  8.0  2000.0  1145.0  1145.0  2198.0  2000.0  3.0  836.0  0.0
 5   50.0  5.0  1993.0   796.0   796.0  1362.0  1993.0  2.0  480.0  1.0
 6   20.0  8.0  2004.0  1686.0  1694.0  1694.0  2004.0  2.0  636.0  0.0
 7   60.0  7.0  1973.0  1107.0  1107.0  2090.0  1973.0  2.0  484.0  1.0
 8   50.0  7.0  1931.0   952.0  1022.0  1774.0  1931.0  2.0  468.0  1.0
 9  190.0  5.0  1939.0   991.0  1077.0  1077.0  1939.0  1.0  205.0  1.0

print(dfci.select_columns_by_values(X_train, kbest_selected_features, n_validation_rows=100, verbose=1))
[
  '1stFlrSF',
  'ExterQual_TA',
  'GarageArea',
  'GarageCars',
  'GarageYrBlt',
  'GrLivArea',
  'MSSubClass',
  'OverallQual',
  'TotalBsmtSF',
  'YearBuilt'
]

X_train = dfci.transform(X_train)
X_test = dfci.transform(X_test)

print(X_train.shape)
(1460, 10)

print(X_test.shape)
(1459, 10)

print(X_train.head(10))
   1stFlrSF  ExterQual_TA  GarageArea  GarageCars  GarageYrBlt  GrLivArea  MSSubClass  OverallQual  TotalBsmtSF  YearBuilt
0     856.0           0.0       548.0         2.0       2003.0     1710.0        60.0          7.0        856.0     2003.0
1    1262.0           1.0       460.0         2.0       1976.0     1262.0        20.0          6.0       1262.0     1976.0
2     920.0           0.0       608.0         2.0       2001.0     1786.0        60.0          7.0        920.0     2001.0
3     961.0           1.0       642.0         3.0       1998.0     1717.0        70.0          7.0        756.0     1915.0
4    1145.0           0.0       836.0         3.0       2000.0     2198.0        60.0          8.0       1145.0     2000.0
5     796.0           1.0       480.0         2.0       1993.0     1362.0        50.0          5.0        796.0     1993.0
6    1694.0           0.0       636.0         2.0       2004.0     1694.0        20.0          8.0       1686.0     2004.0
7    1107.0           1.0       484.0         2.0       1973.0     2090.0        60.0          7.0       1107.0     1973.0
8    1022.0           1.0       468.0         2.0       1931.0     1774.0        50.0          7.0        952.0     1931.0
9    1077.0           1.0       205.0         1.0       1939.0     1077.0       190.0          5.0        991.0     1939.0

print(X_test.head(10))
   1stFlrSF  ExterQual_TA  GarageArea  GarageCars  GarageYrBlt  GrLivArea  MSSubClass  OverallQual  TotalBsmtSF  YearBuilt
0     896.0           1.0       730.0         1.0       1961.0      896.0        20.0          5.0        882.0     1961.0
1    1329.0           1.0       312.0         1.0       1958.0     1329.0        20.0          6.0       1329.0     1958.0
2     928.0           1.0       482.0         2.0       1997.0     1629.0        60.0          5.0        928.0     1997.0
3     926.0           1.0       470.0         2.0       1998.0     1604.0        60.0          6.0        926.0     1998.0
4    1280.0           0.0       506.0         2.0       1992.0     1280.0       120.0          8.0       1280.0     1992.0
5     763.0           1.0       440.0         2.0       1993.0     1655.0        60.0          6.0        763.0     1993.0
6    1187.0           1.0       420.0         2.0       1992.0     1187.0        20.0          6.0       1168.0     1992.0
7     789.0           1.0       393.0         2.0       1998.0     1465.0        60.0          6.0        789.0     1998.0
8    1341.0           1.0       506.0         2.0       1990.0     1341.0        20.0          7.0       1300.0     1990.0
9     882.0           1.0       525.0         2.0       1970.0      882.0        20.0          4.0        882.0     1970.0
```

## dataframe_column_identifier.DataFrameColumnIdentifier
### Creating a new instance

```dfci = DataFrameColumnIdentifier()```

### Methods
- select_columns_by_values :
  
  Returns the names of the Pandas DataFrame columns which are selected based on a matrix of values.
  
  ```dfci.select_columns_by_values(X, selected_values, n_validation_rows=100, verbose=1)```

  Parameters:

  - X : Pandas DataFrame
    
    A DataFrame with the columns that must be found (the DataFrame must have the columns' values either).

  - X_columns_values : numpy matrix 
    
    The values of the columns to be found.

  - n_validation_rows : int, optional (default=1000)
    
    The number of rows that must be equal in the columns comparison. If the informed number is greater than the number of rows in X, the numberrows in X will be used.

  - verbose :  int, optional (default=0)
    
    It controls the verbosity when looking for the columns.

- select_columns_KBest :

  Returns the names of the Pandas DataFrame columns which are selected based on the KBest.get_support method's output.

  ```dfci.select_columns_KBest(X, kbest_get_support_output, verbose=1)```

  Parameters
   
  - X : Pandas DataFrame
    
    The same DataFrame used in the KBest.fit_transform method.

  - kbest_get_support_output : boolean array 
    
    The KBest.get_support method's output.

  - verbose :  int, optional (default=0)
    
    It controls the verbosity when looking for the columns.

- transform : 
  
  Returns a new Pandas DataFrame with only the columns which were selected on the select_columns_* method.

  ```dfci.transform(X)```

  Parameters:

  - X : Pandas DataFrame 
    
    The DataFrame to be transformed (the Pandas DataFrame must have the columns that should be found).

### Attributes
- selected_columns_ : Name of the given Pandas DataFrame columns which were selected based on the given values, after the select_columns_* method execution.
