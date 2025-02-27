import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline
from scipy.stats import pearsonr, f_oneway

def normalize(columnName):
    #a func normalizing data with simple featuring scalling (0-1 range)
    df1[columnName] = df1[columnName]/df1[columnName].max()


def plotHist(columnName, numOfBins, groupNames = []):
    #a func plotting a histogram of a column of interest with the specified number of bins
    #groupNames should be passed on as a list
    bins = np.linspace(min(df1[columnName]), max(df1[columnName]), numOfBins+1)
    newColName = columnName + '-binned'
    df1[newColName] = pd.cut(df1[columnName], bins, labels=groupNames, include_lowest=True)
    
    plt.hist(df1[columnName], bins = bins)
    plt.xlabel(columnName)
    plt.ylabel("count")
    plt.title(columnName + "bins")
    plt.show() 


def convertCatCol(dataframe, columnName):
    #a func creating new True/False (1/0) columns for each unique value in a selected, categorical column and dropping the original, categorical column
    #transforms a column with values: [apple, banana, kiwi] into 3 columns called 'apple', 'banana', 'kiwi' respectively, populating them with Bool vals to show what
    #kid of fruit an entity in a column is. If it's an apple, it'll have a 'True' value in the 'apple' column and 'False' value in the remaining ones
    dummy = pd.get_dummies(dataframe[columnName])
    dataframe = pd.concat([dataframe, dummy], axis=1)
    dataframe.drop(columnName, axis = 1, inplace = True)
    return dataframe


def corrWithPrice(columnName):
#a func that takes in a str name of the column from dataframe to check its correlation with price 

    coef, p_value = pearsonr(df1[columnName], df1['price'])

    #defining if correlation exists based of the correlation coefficient
    if coef <= 0:
        if (coef >= 0) & (coef <= 0.19):
            print('The positive correlation between ', columnName, " and price is very weak.")
        elif (coef >= 0.2) & (coef <= 0.39):
            print('The positive correlation between ', columnName, " and price is weak.")
        elif (coef >= 0.4) & (coef <= 0.59):
            print('The positive correlation between ', columnName, " and price is moderate.")
        else:
            print('The positive correlation between ', columnName, " and price is strong.")
    else:
        if (coef >= -0.19):
            print('The negative correlation between ', columnName, " and price is very weak.")
        elif (coef <= -0.2) & (coef >= -0.39):
            print('The negative correlation between ', columnName, " and price is weak.")
        elif (coef <= -0.4) & (coef >= -0.59):
            print('The negative correlation between ', columnName, " and price is moderate.")
        else:
            print('The negative correlation between ', columnName, " and price is strong.")

    #defining how certain we're about the correlation based on the p-value
    if p_value < 0.001:
        print("The certanity that ", columnName, " has the above correlation with price is very strong.")
    elif p_value < 0.05:
        print("The certanity that ", columnName, " has the above correlation with price is moderately strong.")
    elif p_value < 0.1:
        print("The certanity that ", columnName, " has the above correlation with price is weak.")
    elif p_value > 0.1:
        print("There is no certanity that ", columnName, " has the above correlation with price.")
    
    return [column, coef, p_value]


def ANOVA(columnName):
    #a func that takes in a str name of the column from dataframe to check if there are differences between a category and price due to some
    # random chance or due to some justified reason
    if df1[columnName].dtypes == 'int64' or df1[columnName].dtypes == 'float64':
        f_val, p_val = f_oneway(df1[columnName], df1['price'])

    else:
        grouped=df1.groupby([columnName], observed=True)
        categories = df1[columnName].unique()
        grouped_data = [grouped.get_group(cateogry)['price'] for cateogry in categories]
        f_val, p_val = f_oneway(*grouped_data)

    print( "ANOVA results for", columnName, ": F=", f_val, ", P =", p_val )    
    if p_val > 0.05:
        print("P-value indicates that the findings aren't statistivally significatn." )


def plotMostCorr(corrCol = []):
#a func that visualizes the relationship between the most correlated features and price
#takes in as an argument a list of most correlated column names
    fig, ax = plt.subplots()

    for column in corrCol:
        ax.scatter(df1[column], df1['price'], s = 10, label = column)
    plt.legend(loc = 'lower right')
    plt.show()


def plotResidual(prediction, y_test, modelName):
    #a func to visualize a residual plot of the chosen model
    sns.residplot(x = prediction, y=(y_test - prediction))
    plt.title('Residual plot of a ' + modelName)
    plt.show()


def findBestOrderPoly(highestOrder, x_train, x_test, y_train, y_test):
    if type(highestOrder) == int and highestOrder > 0:
        
        poly_reg = LinearRegression()

        order = []
        Rarr = []
        for i in range(1, highestOrder):
            order.append(i)
        
        for n in order:
            poly = PolynomialFeatures(degree = n)
            X_poly = poly.fit_transform(x_train)
            x_test_poly = poly.transform(x_test)

            poly_reg.fit(X_poly, y_train)
            Yhat_poly = poly_reg.predict(x_test_poly)
            Rarr.append([n, r2_score(y_test, Yhat_poly)])
   
        Rarr_sorted = sorted(Rarr, key= lambda x: (x[1], x[0]), reverse=True)
        
        print('The best order polynomial for this dataset is n= ', Rarr_sorted[0][0], 'with R_sqr value of: ', Rarr_sorted[0][1])

        
    else:
        print('Incorrect order of the polynomial. Choose a positive int.')
    
#---------------------------------------------------------------------------------------------------------------
#data consists no headers
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data'

df = pd.read_csv(url, header = None)

#headers come from https://archive.ics.uci.edu/dataset/10/automobile
headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
         "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
         "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
         "peak-rpm","city-mpg","highway-mpg","price"]
df.columns = headers

#replace missing data
df1 = df.replace('?', np.nan)

allColumns = df1.isnull().sum().sort_values(ascending=False)
missingValuesColumns = []

for key, value in allColumns.items():
    if value > 0:
        missingValuesColumns.append(key)

print("Columns mising values: ", missingValuesColumns)

#convert string to a number as otherwise .astype() cannot be used to change object to fload type of the variable
#missing values need to be in a numeratic format in order to fill them with averages of their columns
for i in range(len(df1.index)):
    if df1.loc[i, 'num-of-doors'] == 'two':
        df1.loc[i, 'num-of-doors'] = 2
    elif df1.loc[i, 'num-of-doors'] == 'four':
        df1.loc[i, 'num-of-doors'] = 4
    else:
        df1.loc[i, 'num-of-doors'] = 0

#convert columns with missing data into numerical values to replace missing values with the column mean
for column in missingValuesColumns:
    df1[column] = df1[column].astype('float')
    
    #ignore the warning about using exact values to use the above 'replace' function - it's going to be depreciated
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        
        #replace missing values with column mean
        df1[column].replace(np.nan, df1[column].mean(), inplace = True)
    
    
# Convert mpg to L/100km by mathematical operation (235 divided by mpg)
#drop the city-mpg and highway-mpg columns as they're not needed - new values are in new columns
#renaming city-mpg to city-L/100km would create a duplicate column
df1['city-L/100km'] = 235/df1["city-mpg"]
df1 = df1.drop('city-mpg', axis=1)

df1['highway-L/100km'] = 235/df1['highway-mpg']
df1 = df1.drop('highway-mpg', axis=1)

#normalize columns
df1['length'] = normalize('length')
df1['width'] = normalize('width')
df1['height'] = normalize('height')


#plotting binned data
group_names = ['low', 'medium', 'high']
#plotHist(columnName= 'horsepower', numOfBins = 3, groupNames=group_names)


#conver categorical columns into bool dummies
df1 = convertCatCol(df1, 'fuel-type')
df1 = convertCatCol(df1, 'aspiration')
print(df1.columns)


corrResults= []
#correlation between numerical categories and price - correlation prive with price = 1, therefore omitted
for column in df1.columns:
    if column != 'price':
        if df1[column].dtypes == int or df1[column].dtype == float:
            corrResults.append(corrWithPrice(column))

corrResults_sorted = sorted(corrResults, key= lambda x: (x[2], x[1]))

print('The strongest correlation (positive or negative) with price show: ')
for result in corrResults_sorted:
    print('category:', result[0], 'with correlation coeff: ', result[1], 'and p-value: ', result[2], '.')


#ANOVA testing
""" for column in df1.columns:
    if column != 'price':
        ANOVA(column) """


mostCorrColumns = []
for i in range(5):
    mostCorrColumns.append(corrResults_sorted[i][0])

print(mostCorrColumns)
#visualize the relationship between the most correlated features and price
#plotMostCorr(mostCorrColumns)

#--------------------------------------------------------------------------

#splitting the data into training and test sets
numData = []
for column in df1.columns:
    if df1[column].dtypes == int or df1[column].dtypes == float and column != 'price':
        numData.append(column)

X = df1[numData]
y = df1['price']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#fit a mumtiple linear regression model
lm = LinearRegression()
lm.fit(x_train, y_train)
Yhat = lm.predict(x_test) #prediction

R_sqr_MLR = r2_score(y_test, Yhat)
print('multiple linear regression R_sqr: R', R_sqr_MLR)


#visualize residual plot of the linear regression model
#plotResidual(Yhat, y_test, 'multiple linear regression')
#---------------------------------------------------------------------

#find best order for a polynomial to represent the data
findBestOrderPoly(6, x_train, x_test, y_train, y_test)

# Define pipeline for polynomial regression
pipeline = Pipeline([
    ('poly_features', PolynomialFeatures(degree=2)),  # Replace with desired degree
    ('scaler', StandardScaler()),  # Optional: scaling the features
    ('linear_regression', LinearRegression())
])

pipeline.fit(x_train, y_train)
Yhat_poly = pipeline.predict(x_test)
print("polynomial regression R_sqr ", r2_score(y_test, Yhat_poly))

#ridge
ridge = Ridge(alpha=1)
ridge.fit(x_train, y_train)
y_pred = ridge.predict(x_test)
print("ridge regression R_sqr ", r2_score(y_test, y_pred))
 
sns.kdeplot(Yhat, label = 'Linear regression')
sns.kdeplot(Yhat_poly, label = 'polynomialregression , order 2')
sns.kdeplot(y_pred, label = 'ridge regression')
sns.kdeplot(df1['price'], label = 'actual prices')
plt.legend(loc = 'lower right')
plt.show() 

#plotResidual(y_pred, y_test, 'ridge regression')
#plotResidual(Yhat_poly, y_test, 'polynomial regression, order 2')


#download edited CVS to the working direcotyr
#df1.to_csv('data')
