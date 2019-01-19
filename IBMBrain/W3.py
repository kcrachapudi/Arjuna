import pandas as pd
import numpy as np
from scipy import stats
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
# 3. Correlation
# 4. Correlation - Statistics
# 5. ANOVA

dfWithHeaders = None
dfList = []
dfTables = []
graphs = []
dfInfos = []
notifications = []

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
    elif unit == 5:
        ANOVA()
    ProcessHTML()
    return

def DescriptiveStatistics():
    global dfWithHeaders, dfInfos, dfList, graphs
    dataframer = DataFramer()
    htmlHelper = HTMLHelper()
    charter = Charter()
    #Show basic Information about DataFrame
    info1 = dataframer.DataFrameInfo(dfWithHeaders)
    dfInfos.append(dfInfo)

    #Describe basic features of Data
    #Giving short summaries about the sample and measures of the data
    #Summarize statistics using the pandas describe() function
    dfDescription = dfWithHeaders.describe()
    dfList.append( ("Auto Data Descriptive Statistics with Describe", dfDescription, True) )

    #Summarize categorical data using value_counts() method
    drivewheelcounts = dfWithHeaders["drive-wheels"].value_counts()
    print("drivewheelcounts ")
    print(drivewheelcounts)
    dfdrivewheelcounts = pd.DataFrame([drivewheelcounts])
    dfList.append( ("Auto Data Drive Wheel Counts", dfdrivewheelcounts, True))
    
    #BoxPlot
    dfNumCleaned = dfWithHeaders.copy(deep=True)
    #Box plot of price column
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "price", coltype = "int64")
    xaxis = "price"
    boxplot = charter.BoxPlot(xaxis, dfNumCleaned, "png")
    graphs.append(boxplot)
    #Box plot of engine-size column    
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "engine-size", coltype = "int64")
    xaxis = "engine-size"
    boxplot2 = charter.BoxPlot(xaxis, dfNumCleaned, "png")
    graphs.append(boxplot2)
    #Boxplot with two variables
    xaxis = "drive-wheels"
    yaxis = "price"
    boxplot3 = charter.BoxPlot2(xaxis, yaxis, dfNumCleaned, "png")
    graphs.append(boxplot3)
    #Show basic Information about new cleaned DataFrame
    info2 = dataframer.DataFrameInfo(dfNumCleaned)
    dfInfos.append(info2)
    #ScatterPlot
    #Each observation represented as a point
    #Scatter plots show the relationship between two variables
    #Predictor/independent variable on x-axis
    #Target/dependent variable on y-axis
    xaxis = "engine-size"
    yaxis = "price"
    scatterplot = charter.ScatterPlot(xaxis = xaxis, yaxis = yaxis, dfData = dfNumCleaned)
    graphs.append(scatterplot)
    return

def GroupBy():
    #Groupby can be applied on Categorical variables; Group data into categories; Group by single or multiple variables
    global dfWithHeaders, dfInfos, dfList, graphs
    dataframer = DataFramer()
    htmlHelper = HTMLHelper()
    charter = Charter()
    #Get DataFrame and Clean Numeric Data
    dfNumCleaned = dfWithHeaders.copy(deep=True)
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "price", coltype = "int64")
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "engine-size", coltype = "int64")
    #Get the columns we are interested in
    dfFiltered = dfNumCleaned["drive-wheels"].to_frame()
    dfFiltered["body-style"] = dfNumCleaned["body-style"]
    dfFiltered["price"] = dfNumCleaned["price"]
    info2 = dataframer.DataFrameInfo(dfFiltered)
    dfInfos.append(info2)
    #GROUPBY AVERAGE
    #One column grouping
    dfGroup = dfFiltered.groupby(["drive-wheels"], as_index = False).mean()
    dfList.append( ("Grouped by drive-wheels Dataframe", dfGroup, True) )
    #This is a sub group within a group
    dfGroup2 = dfFiltered.groupby(["drive-wheels", "body-style"], as_index = False).mean()
    dfList.append("Grouped by drive-wheels and sub grouped on body-style", dfGroup2, True)
    #GROUPBY TOTAL 
    #One column grouping
    dfGroup = dfFiltered.groupby(["drive-wheels"], as_index = False).sum()
    dfList.append("Grouped by drive-wheels Dataframe", dfGroup, True)
    #This is a sub group within a group
    dfGroup2 = dfFiltered.groupby(["drive-wheels", "body-style"], as_index = False).sum()
    #The Groupby subgrouped grid only shows data if it is existing
    dfList.append("Grouped by drive-wheels and sub grouped on body-style", dfGroup2, True)
    # PIVOT To show the same grouped data on 2 variables in a rectangular grid use the pivot method
    #The Pivot grid forces to show all data even if it is empty
    dfPivot = dfGroup2.pivot(index = "drive-wheels", columns = "body-style")
    #The Pivot grid shows numcolA * numcolB number of cells in the grid
    #The Pivot grid is similar to an Excel Spreadsheet
    dfList.append("Pivot the sub-grouped df into a rectangular grid", dfPivot, True)
    #HEATMAP
    #Heatmap takes a rectangular grid of data (pivot grid or excel)
    #It assigns a color intensity based on the value on the grid
    #Plot the target variable over multiple variables
    heatmap = charter.HeatMap(dfData = dfPivot)
    graphs.append(heatmap)
    #Seaborn heatmap
    heatmap2 = charter.HeatMapSNS(dfData = dfPivot)
    graphs.append(heatmap2)
    return

def Correlation():
    #Correlation measures to what extent different variables are interdependent.
    global dfWithHeaders, dfInfos, dfList, graphs
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
    dfInfos.append(info)
    #Lung Canceer and Smoking are correlated; Rain and Umbrella usage are interdependent(correlated)
    #CORRELATION DOES NOT IMPLY CAUSATION
    #Positive Linear Relationship
    #Correlation between engine-size and price
    chart1 = charter.RegPlot(xaxis = "engine-size", yaxis = "price", dfData = dfNumCleaned)
    #There is a line in the chart called the Regression line that indicates the relationship between the two variables
    graphs.append(chart1)
    #Negative Linear Relationship
    #Correlation between highway-mpg and price
    chart2 = charter.RegPlot(xaxis = "highway-mpg", yaxis = "price", dfData = dfNumCleaned)
    #There is a line in the chart called the Regression line that indicates the relationship between the two variables
    graphs.append(chart2)
    #Weak Correlation: As long as the slope of the line is steep we can say there is a positive or negative correlation. 
    #If the slope of the line is flattish then we can say there is no correlation
    chart3 = charter.RegPlot(xaxis = "peak-rpm", yaxis = "price", dfData = dfNumCleaned)
    #There is a line in the chart called the Regression line that indicates the relationship between the two variables
    graphs.append(chart3)    
    return

def CorrelationStatistics():
    global dfWithHeaders, dfInfos, dfList, graphs, notifications
    dataframer = DataFramer()
    htmlHelper = HTMLHelper()
    charter = Charter()
    #Get DataFrame and Clean Numeric Data
    dfNumCleaned = dfWithHeaders.copy(deep=True)
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "price", coltype = "int64")
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "horsepower", coltype = "int64")
    info = dataframer.DataFrameInfo(dfNumCleaned)
    dfInfos.append(info)
    #Pearson Correlation: Measure the strength of the correlation between two features
    # Correlation Coefficient: Close to +1 Large Positive Correlation; Close to -1 Large Negative Correlation; Close to 0 No Correlation
    # P-value <0.001 Strong certainty in result; <0.05 Moderate certainty in the result; <0.1 Weak certainty in result; >0.1 No certainty in result
    # STRONG CORRELATION: Correlation Coefficient close to 1 or -1 and P-value less than 0.001
    PearsonCoeff, PValue = stats.pearsonr(dfNumCleaned["horsepower"], dfNumCleaned["price"])
    notifications.append("PearsonCoeff is " + str(PearsonCoeff))
    notifications.append("PValue is " + str(PValue))
    #Correlation Heatmap of all variables to all variables
    #This gives a negative correlation line as each variable is mapped to itself in the middle negative line
    return

def ANOVA():
    global dfWithHeaders, dfInfos, dfList, graphs, notifications
    dataframer = DataFramer()
    htmlHelper = HTMLHelper()
    charter = Charter()
    #Get DataFrame and Clean Numeric Data
    dfNumCleaned = dfWithHeaders.copy(deep=True)
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "price", coltype = "int64")
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "horsepower", coltype = "int64")
    info = dataframer.DataFrameInfo(dfNumCleaned)
    dfInfos.append(info)
    #Analysis of Variance ANOVA
    # We perform ANOVA to Find Correlation between different groups of a categorical variable
    # What we obtain from ANOVA
    # F-test score: variation between sample group means divided by variation within sample group
    # p-value: confidence degree
    
    dfAnova = dfNumCleaned[["make", "price"]]
    dfAnovaGrouped = dfAnova.groupby(["make"])

    # ANOVA between Honda and Subaru
    anovaresults1 = stats.f_oneway( dfAnovaGrouped.get_group("honda")["price"], dfAnovaGrouped.get_group("subaru")["price"] )
    notifications.append(anovaresults1)

    # ANOVA between Honda and Jaguar
    anovaresults2 = stats.f_oneway( dfAnovaGrouped.get_group("honda")["price"], dfAnovaGrouped.get_group("jaguar")["price"] )
    notifications.append(anovaresults2)

    #Comparing the two ANOVA results say that there is a strong correlation between a categorical variable and other variables, 
    # if the ANOVA test gives us a large F-test value and a small p-value.

    return

def ProcessHTML():
    global dfList, dfTables
    htmlHelper = HTMLHelper()
    for tuple in dfList:
        dfName = tuple[0]
        dfTable = htmlHelper.GetHTMLTableFromDataFrame(tuple[1], None, tuple[2])
        dfTables.append((dfName, dfTable))

