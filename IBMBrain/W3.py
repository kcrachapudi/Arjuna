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
        GroupBy()
    elif unit == 3:
        Correlation()
    elif unit == 4:
        CorrelationStatistics()
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

def GroupBy():
    #Groupby can be applied on Categorical variables; Group data into categories; Group by single or multiple variables
    global dfWithHeaders
    dataframer = DataFramer()
    htmlHelper = HTMLHelper()
    charter = Charter()
    #Get DataFrame and Clean Numeric Data
    dfNumCleaned = dfWithHeaders.copy(deep=True)
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "price", coltype = "int64")
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "engine-size", coltype = "int64")
    info = dataframer.DataFrameInfo(dfNumCleaned)
    AddDFInfoToList(info)
    #Get the columns we are interested in
    dfFiltered = dfNumCleaned["drive-wheels"].to_frame()
    dfFiltered["body-style"] = dfNumCleaned["body-style"]
    dfFiltered["price"] = dfNumCleaned["price"]
    info2 = dataframer.DataFrameInfo(dfFiltered)
    AddDFInfoToList(info2)
    #GROUPBY AVERAGE
    #One column grouping
    dfGroup = dfFiltered.groupby(["drive-wheels"], as_index = False).mean()
    AddDFtoList("Grouped by drive-wheels Dataframe", dfGroup, True)
    #This is a sub group within a group
    dfGroup2 = dfFiltered.groupby(["drive-wheels", "body-style"], as_index = False).mean()
    AddDFtoList("Grouped by drive-wheels and sub grouped on body-style", dfGroup2, True)
    #GROUPBY TOTAL 
    #One column grouping
    dfGroup = dfFiltered.groupby(["drive-wheels"], as_index = False).sum()
    AddDFtoList("Grouped by drive-wheels Dataframe", dfGroup, True)
    #This is a sub group within a group
    dfGroup2 = dfFiltered.groupby(["drive-wheels", "body-style"], as_index = False).sum()
    #The Groupby subgrouped grid only shows data if it is existing
    AddDFtoList("Grouped by drive-wheels and sub grouped on body-style", dfGroup2, True)
    # PIVOT To show the same grouped data on 2 variables in a rectangular grid use the pivot method
    #The Pivot grid forces to show all data even if it is empty
    dfPivot = dfGroup2.pivot(index = "drive-wheels", columns = "body-style")
    #The Pivot grid shows numcolA * numcolB number of cells in the grid
    #The Pivot grid is similar to an Excel Spreadsheet
    AddDFtoList("Pivot the sub-grouped df into a rectangular grid", dfPivot, True)
    #HEATMAP
    #Heatmap takes a rectangular grid of data (pivot grid or excel)
    #It assigns a color intensity based on the value on the grid
    #Plot the target variable over multiple variables
    heatmap = charter.HeatMap(dfData = dfPivot)
    AddGraphToList(heatmap)
    #Seaborn heatmap
    heatmap2 = charter.HeatMapSNS(dfData = dfPivot)
    AddGraphToList(heatmap2)
    return

def Correlation():
    #Correlation measures to what extent different variables are interdependent.
    global dfWithHeaders
    dataframer = DataFramer()
    htmlHelper = HTMLHelper()
    charter = Charter()
    #Get DataFrame and Clean Numeric Data
    dfNumCleaned = dfWithHeaders.copy(deep=True)
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "price", coltype = "int64")
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "engine-size", coltype = "int64")
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "highway-mpg", coltype = "int64")
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "peak-rpm", coltype = "int64")
    info = dataframer.DataFrameInfo(dfNumCleaned)
    AddDFInfoToList(info)
    #Lung Canceer and Smoking are correlated; Rain and Umbrella usage are interdependent(correlated)
    #CORRELATION DOES NOT IMPLY CAUSATION
    #Positive Linear Relationship
    #Correlation between engine-size and price
    chart1 = charter.RegPlot(xaxis = "engine-size", yaxis = "price", dfData = dfNumCleaned)
    #There is a line in the chart called the Regression line that indicates the relationship between the two variables
    AddGraphToList(chart1)
    #Negative Linear Relationship
    #Correlation between highway-mpg and price
    chart1 = charter.RegPlot(xaxis = "highway-mpg", yaxis = "price", dfData = dfNumCleaned)
    #There is a line in the chart called the Regression line that indicates the relationship between the two variables
    AddGraphToList(chart1)
    #Weak Correlation: As long as the slope of the line is steep we can say there is a positive or negative correlation. 
    #If the slope of the line is flattish then we can say there is no correlation
    chart1 = charter.RegPlot(xaxis = "peak-rpm", yaxis = "price", dfData = dfNumCleaned)
    #There is a line in the chart called the Regression line that indicates the relationship between the two variables
    AddGraphToList(chart1)
    
    return

def CorrelationStatistics():
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
