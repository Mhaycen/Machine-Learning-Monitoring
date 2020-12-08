import pandas as pd 
import numpy as np  
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn import metrics

#importing dataset from sklearn
from sklearn.datasets import load_boston
boston_data = load_boston()

#initializing dataset
# pylint: disable=maybe-no-member
data_ = pd.DataFrame(boston_data.data)
data_.head()
#adding feature names to the dataframe
data_.columns = boston_data.feature_names

# Target variable of Boston Housing data

data_['PRICE'] = boston_data.target
# creating feature and target variable

X = data_.drop(['PRICE'], axis=1)
y = data_['PRICE']

# splitting into training and testing set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=1)
print("X training shape : ", X_train.shape )
print("X test shape : ", X_test.shape)
print("y training shape :", y_train.shape )
print(" y test shape : ", y_test.shape )

#creating model
from sklearn.ensemble import RandomForestRegressor
classifier = RandomForestRegressor()
classifier.fit(X_train, y_train)

#Model evaluation for training data
prediction = classifier.predict(X_train)
print("r^2 : ", metrics.r2_score(y_train, prediction))
print("Mean Absolute Error: ", metrics.mean_absolute_error(y_train, prediction))
print("Mean Squared Error: ", metrics.mean_squared_error(y_train, prediction))
print("Root Mean Squared Error: ", np.sqrt(metrics.mean_squared_error(y_train, prediction)))

# Model evaluation for testing data
prediction_test = classifier.predict(X_test)
print("r^2 : ", metrics.r2_score(y_test, prediction_test))
print("Mean Absolute Error : ", metrics.mean_absolute_error(y_test, prediction_test))
print("Mean Squared Error : ", metrics.mean_squared_error(y_test, prediction_test))
print("Root Mean Absolute Error : ", np.sqrt(metrics.mean_squared_error(y_test, prediction_test)))

#saving model 
import pickle
with open('webapp/model/models.pkl','wb') as file:
    pickle.dump(classifier, file)

#saving the columns
model_columns = list(X.columns)
with open('webapp/model/model_columns.pkl','wb') as file:
    pickle.dump(model_columns, file)