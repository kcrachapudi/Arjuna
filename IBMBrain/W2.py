
#For one reason or another, it may be useful to keep that observation even if some features are missing. Now, let's go into how to drop missing values or replace missing values in Python. 
#To remove data that contains missing values Panda's library has a built-in method called dropna. 
#Essentially, with the dropna method, you can choose to drop rows or columns that contain missing values like NaN. 
#So you'll need to specify access equal zero to drop the rows or access equals one to drop the columns that contain the missing values. 
#In this example, there is a missing value in the price column. Since the price of used cars is what we're trying to predict in our upcoming analysis, we have to remove the cars,
#the rows, that don't have a listed price. It can simply be done in one line of code using dataframe.dropna. Setting the argument in place to true, allows the modification to be
#done on the data set directly. In place equals true, just writes the result back into the data frame. This is equivalent to this line of code. 
#Don't forget that this line of code does not change the data frame but is a good way to make sure that you are performing the correct operation. 
#To modify the data frame, you have to set the parameter in place equal to true. You should always check the documentation if you are not familiar with the function or method. 
#The pandas web page has lots of useful resources. To replace missing values like NaNs with actual values, Pandas library has a built-in method called replace
#which can be used to fill in the missing values with the newly calculated values. 
#As an example, assume that we want to replace the missing values of the variable normalized losses by the mean value of the variable.
#Therefore, the missing value should be replaced by the average of the entries within that column. In Python, first we calculate the mean of the column. 
#Then we use the method replace to specify the value we would like to be replaced as the first parameter, in this case NaN. 
#The second parameter is the value we would like to replace it with i.e the mean in this example. This is a fairly simplified way of replacing missing values. 
#There are of course other techniques such as replacing missing values for the average of the group instead of the entire data set. 
#So, we've gone through two ways in Python to deal with missing data. We learnt to drop problematic rows or columns containing missing values 
#and then we learnt how to replace missing values with other values. But don't forget the other ways to deal with missing data. 
#You can always check for a higher quality data set or source or in some cases you may want to leave the missing data as missing data.

# Data Acquisition
import pandas as pd
import numpy as np
import Utils
from Utils import FileProcessor, HTMLHelper

FileURL = None
LocalPath = "../Data/"
FileName = "AutosData85Headers.csv"
FileType = "csv"
SaveLocal = None

#Autos Dataframes
dfWithHeaders = None
dfWithoutPrice = None

dfList = []
dfTables = []

def ProcessAutosData(unit):
    global FileURL, LocalPath, FileName, FileType, SaveLocal, dfWithHeaders, dfWithoutPrice
    fileProcessor = FileProcessor(LocalPath, FileName, FileType, None, None)
    dfWithHeaders = fileProcessor.ReadFile()
    AddDFtoList("Auto Data With Headers", dfWithHeaders)
    if(unit is not None):
        unit = int(unit)
    if unit == 1:
        BasicMissingReplacingData()
    elif unit == 2:
        FormattingAndNormalizingData()
    elif unit == 3:
        BinningData()
    elif unit == 4:
        CategoricalToQuantitativeData()
    ProcessHTML()
    return

def BasicMissingReplacingData():
    global dfWithHeaders

    #Drop missing values along the column 'price    
    dfWithoutPrice = dfWithHeaders.copy(deep=True)
    #axis=0 drops the rows with na values. if subset is not mentioned then it dropws any row that has any na column value
    #inplace = True is to reassign the changed dataframe to the original dataframe without a need to assignment
    #dfWithoutPrice.dropna(subset=["price"], axis=0, inplace = True)   
    #dfWithoutPrice.dropna(subset=["price"], axis=1, inplace = True)   
    #AddDFtoList("Auto Data with Deleted Null Prices", dfWithoutPrice)

    dfPriceReplaceNAWithZero = dfWithHeaders.copy(deep = True)
    #print(dfPriceReplaceNAWithMean.dtypes)
    #The price column is an object column so to do any calculations on it we have to convert it to numeric 
    # convert from object to string to numeric
    #dfPriceReplaceNAWithMean["price"] = dfPriceReplaceNAWithMean["price"].astype(str).astype(int)
    #The values all have to be numeric for the conversion to work. 
    #We can first replace the missing values with a default and then do conversions if needed
    dfPriceReplaceNAWithZero["price"].replace('?', 0, inplace = True)
    dfPriceReplaceNAWithZero["price"].replace(np.nan, 0, inplace = True)
    AddDFtoList("Auto Data with missing Price replaced with Zero", dfPriceReplaceNAWithZero)
    
    dfPriceReplaceNAWithMean = dfPriceReplaceNAWithZero.copy(deep = True)
    dfPriceReplaceNAWithMean["price"] = dfPriceReplaceNAWithMean["price"].astype(int)
    meanprice = dfPriceReplaceNAWithMean["price"].mean().astype(int)
    dfPriceReplaceNAWithMean["price"].replace(0, meanprice, inplace = True)
    AddDFtoList("Auto Data with missing Price replaced with Mean", dfPriceReplaceNAWithMean)
    return

def FormattingAndNormalizingData():
    global dfWithHeaders

    #Convert city-mpg to L/100km in the car dataset as it is used in many countries
    dfL100Km = dfWithHeaders.copy(deep=True)
    dfL100km["city-L/100km"] = 235/dfWithHeaders["city-mpg"]
    AddDFtoList("Auto Data with city-mpg and city-L/100KM", dfL100Km)
    #You can also convert the same column and rename it if you don't need to keep both
    #dfL100km["city-mpg"] = 235/dfWithHeaders["city-mpg"]
    #dfL100km.rename(columns={"city-mpg":"city-L/100Km"}, inplace = True)

    #Data Normalization

    #Simple Feature Scaling Values range between 0 to 1
    #xnew = xold/xmax
    dfNormalization = dfWithHeaders.copy(deep=True)
    dfNormalization["length-simplefeaturescaling"] = dfNormalization["length"] / dfNormalization["length"].max()
    #Min Max  Values range between 0 to 1
    #xnew  = (xold-xmin)/(xmax-xmin)
    dfNormalization["length-minmax"] = (dfNormalization["length"] - dfNormalization["length"].min())/(dfNormalization["length"].max() - dfNormalization["length"].min())
    #Z-score Values range between -3 to 3 typically but could vary
    #xnew = (xold-xavg)/xstd
    dfNormalization["length-zscore"] = (dfNormalization["length"] - dfNormalization["length"].mean())/(dfNormalization["length"].std())

    AddDFtoList("Simple Feature Scaling Normalization of length", dfNormalization)
    return

def BinningData():
    global dfWithHeaders
    # Data Binning
    #Binning is Grouping of values into Bins; Converts Numeric to Categorical variables; Group a numeric set of values into a set of bins
    # price has a distribution from 4000 to 50000 roughly. Instead we could bin them into Low, Medium and High
    dfPriceBinned = dfWithHeaders.copy(deep=True)
    #cleanup the price column by converting any ? to 0
    dfPriceBinned["price"].replace('?', 0, inplace = True)
    #Convert the price column from object to numeric
    dfPriceBinned["price"] = pd.to_numeric(dfPriceBinned["price"], "coerce")
    #Convert any NaN values that were coerced to 0
    dfPriceBinned["price"].replace(np.nan, 0, inplace = True)
    #Ensure that the price column is integer
    dfPriceBinned["price"] = dfPriceBinned["price"].astype("int64")
    maxprice = dfPriceBinned["price"].max()
    minprice = dfPriceBinned["price"].min()
    pricebinwidth = int((maxprice + 10 - minprice)/3) #The number of bins required (Low, Med, High) 
    pricebins = range(minprice-5, maxprice+5, pricebinwidth) #Create the bin values
    print("maxprice " + str(maxprice))
    print("minprice " + str(minprice))
    print("pricebinwidth " + str(pricebinwidth))
    print("pricebins " + str(pricebins))
    pricebinnames = ["Low", "Medium", "High"] #Create bin names
    dfPriceBinned["price-binned"] = pd.cut(dfPriceBinned["price"], pricebins, labels = pricebinnames)
    AddDFtoList("Auto Data with price-binned", dfPriceBinned)
    return

def CategoricalToQuantitativeData():
    global dfWithHeaders
    dfCatToQuant = dfWithHeaders.copy(deep=True)
    # Categorical to Quantitative
    # For example Category Fuel has Gas or Diesel. Converting this would get two new (dummy) columns gas and diesel 
    # If the original Fuel category had "Gas" then the new column "gas" would have 1 and "diesel" would have 0
    # This is called "One Hot Encoding"
    # pandas.get_dummies() is used to do the conversion from categorical to dummy variables
    #This just returns a new dataframe with the dummy columns
    dfDummy = pd.get_dummies(dfCatToQuant["fuel-type"])
    print(dfDummy)
    #To add the new columns to the existing dataframe use the concat function
    dfCatToQuant = pd.concat([dfCatToQuant, pd.get_dummies(dfCatToQuant["fuel-type"], prefix="fuel-type-")], axis = 1)
    #Drop the original fuel-type column as we don't need it anymore. keeping it would be like having dependency colums in the same table
    dfCatToQuant.drop(["fuel-type"], axis = 1, inplace = True)
    AddDFtoList("Auto Data Fuel Categorical to Quantitative", dfCatToQuant)
    return

def AddDFtoList(dfName, df):
    global dfList
    dfTuple = (dfName, df)
    dfList.append(dfTuple)
    return

def ProcessHTML():
    global dfList, dfTables
    htmlHelper = HTMLHelper()
    for tuple in dfList:
        dfName = tuple[0]
        dfTable = htmlHelper.GetHTMLTableFromDataFrame(tuple[1])
        dfTables.append((dfName, dfTable))