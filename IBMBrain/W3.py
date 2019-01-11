import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Utils
from Utils import *

FileURL = None
LocalPath = "../Data/"
FileName = "AutosData85Headers.csv"
FileType = "csv"
SaveLocal = None

#Exploratory Data Analysis
#Preliminary Steps
# 1. Summarize main characteristics of the data
# 2. Gain better understanding of the data set
# 3. Uncover relationships between variables
# 4. Extract important variables
# The Question we wil try to answer is
# What are the characteristics that have the most impact on the car price?

# Learning Objectives
# 1. Descriptive Statistics
# 2. GroupBy
# 3. ANOVA
# 4. Correlation
# 5. Correlation - Statistics

dfWithHeaders = None
dfList = []
dfTables = []
graphs = []
dfInfos = []
def ProcessAutosData(unit):
    global FileURL, LocalPath, FileName, FileType, SaveLocal, dfWithHeaders
    fileProcessor = FileProcessor(LocalPath, FileName, FileType, None, None)
    dfWithHeaders = fileProcessor.ReadFile()
    if(unit is not None):
        unit = int(unit)
    if unit == 1:     
        DescriptiveStatistics()
    elif unit == 2:
        FormattingAndNormalizingData()
    elif unit == 3:
        BinningData()
    elif unit == 4:
        CategoricalToQuantitativeData()
    ProcessHTML()
    return

def DescriptiveStatistics():
    global dfWithHeaders
    dataframer = DataFramer()
    htmlHelper = HTMLHelper()
    charter = Charter()
    #Show basic Information about DataFrame
    info1 = dataframer.DataFrameInfo(dfWithHeaders)
    AddDFInfoToList(info1)

    #Describe basic features of Data
    #Giving short summaries about the sample and measures of the data
    #Summarize statistics using the pandas describe() function
    dfDescription = dfWithHeaders.describe()
    AddDFtoList("Auto Data Descriptive Statistics with Describe", dfDescription, True)

    #Summarize categorical data using value_counts() method
    drivewheelcounts = dfWithHeaders["drive-wheels"].value_counts()
    print("drivewheelcounts ")
    print(drivewheelcounts)
    dfdrivewheelcounts = pd.DataFrame([drivewheelcounts])
    AddDFtoList("Auto Data Drive Wheel Counts", dfdrivewheelcounts, True)
    
    #BoxPlot
    dfNumCleaned = dfWithHeaders.copy(deep=True)
    #Box plot of price column
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "price", coltype = "int64")
    xaxis = "price"
    boxplot = charter.BoxPlot(xaxis, dfNumCleaned, "png")
    AddGraphToList(boxplot)
    #Box plot of engine-size column    
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "engine-size", coltype = "int64")
    xaxis = "engine-size"
    boxplot2 = charter.BoxPlot(xaxis, dfNumCleaned, "png")
    AddGraphToList(boxplot)
    #Boxplot with two variables
    xaxis = "drive-wheels"
    yaxis = "price"
    boxplot2 = charter.BoxPlot2(xaxis, yaxis, dfNumCleaned, "png")
    AddGraphToList(boxplot2)
    #Show basic Information about new cleaned DataFrame
    info2 = dataframer.DataFrameInfo(dfNumCleaned)
    AddDFInfoToList(info2)
    #ScatterPlot
    #Each observation represented as a point
    #Scatter plots show the relationship between two variables
    #Predictor/independent variable on x-axis
    #Target/dependent variable on y-axis
    xaxis = "engine-size"
    yaxis = "price"
    scatterplot = charter.ScatterPlot(xaxis = xaxis, yaxis = yaxis, dfData = dfNumCleaned)
    AddGraphToList(scatterplot)
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

def AddDFtoList(dfName, df, dfIndexer = False):
    global dfList
    dfTuple = (dfName, df, dfIndexer)
    dfList.append(dfTuple)
    return

def ProcessHTML():
    global dfList, dfTables
    htmlHelper = HTMLHelper()
    for tuple in dfList:
        dfName = tuple[0]
        dfTable = htmlHelper.GetHTMLTableFromDataFrame(tuple[1], None, tuple[2])
        dfTables.append((dfName, dfTable))

def AddGraphToList(graph):
    global graphs
    graphs.append(graph)
    return

def AddDFInfoToList(dfInfo):
    global dfInfos
    dfInfos.append(dfInfo)
    return
