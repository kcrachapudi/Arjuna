import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import sklearn
from sklearn.linear_model import LinearRegression
import Utils
from Utils import *

FileURL = "https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DA0101EN/automobileEDA.csv"
LocalPath = "../Data/"
FileName = "CognitiveClassAutos.csv"
FileType = "csv"
SaveLocal = None

dfWithHeaders = None
dfCogAutos = None
dfList = []
dfTables = []
graphs = []
dfInfos = []
notifications = []

# Learning Objectives
# Simple and Multiple Linear Regression
# Model Evaluation using Visualization
# Polynomial Regression and Pipelines
# R-squared and MSE for In-Sample Evaluation
# Prediction and Decision Making
# How can you determine a fair value for a used car

#A Model can be thought of as a mathematical equation used to predict a value, given one or more other values

# Independent Variables of Features ->>>  Model   ->>>>  Dependent Variables
#  highway-mpg of Car ->>>> Model ->>>>> Predicted Price of Car
 
# Usually the more relevant data you have the more accurate your Model is
# More the data, more the accuracy of the Model 

def ProcessAutosData(unit):
    global FileURL, LocalPath, FileName, FileType, SaveLocal, dfWithHeaders, dfCogAutos
    fileProcessor = FileProcessor(LocalPath, FileName, FileType, FileURL, True)
    dfCogAutos = fileProcessor.ReadFile()
    if(unit is not None):
        unit = int(unit)
    if unit == 1:     
        FileName = "AutosData85Headers.csv"
        fileProcessor = FileProcessor(LocalPath, FileName, FileType, FileURL, True)
        dfWithHeaders = fileProcessor.ReadFile()
        SimpleLinearRegression()
    elif unit == 2:
        FileName = "AutosData85Headers.csv"
        fileProcessor = FileProcessor(LocalPath, FileName, FileType, FileURL, True)
        dfWithHeaders = fileProcessor.ReadFile()
        MultipleLinearRegression()
    elif unit == 3:
        FileName = "CognitiveClassAutos.csv"
        fileProcessor = FileProcessor(LocalPath, FileName, FileType, FileURL, True)
        dfCogAutos = fileProcessor.ReadFile()
        ModelDevelopment()
    elif unit == 4:
        FileName = "CognitiveClassAutos.csv"
        fileProcessor = FileProcessor(LocalPath, FileName, FileType, FileURL, True)
        dfCogAutos = fileProcessor.ReadFile()
        PolynomialRegression()
    return

def SimpleLinearRegression():
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

    # Simple Linear Regression (SLR)
    # Simple Linear Regression will refer to one Independent variable to make a prediction
    # SLR tries to show a relationship between a predictor variable x and a target variable y
    # y = b0 + b1 * x, the parameter b0 is the Intercept and the parameter b1 is the slope
    lm = LinearRegression()
    # Define the Predictor Variable
    X = dfNumCleaned[["highway-mpg"]]
    # Define the Target Variable
    Y = dfNumCleaned[["price"]]
    # Use lm.fit(X, Y) to fit the Model, i.e. find the parameters b0 and b1
    lm.fit(X, Y)
    # We can obtain a prediction
    Yhat = lm.predict(X)
    print(Yhat)
    print(lm.intercept_) # gives the variable b0
    print(lm.coef_) # gives the slope
    # The relationship between price and highway-mpg is given by
    # Price = lm.intercept - lm.coef * highway-mpg
    return

def MultipleLinearRegression():
    import sklearn
    from sklearn.linear_model import LinearRegression
    global dfWithHeaders, dfInfos, dfList, graphs
    dataframer = DataFramer()
    htmlHelper = HTMLHelper()
    charter = Charter()
    # Multiple Linear Regression
    # This will refer to multiple independent variables to make a prediction
    # This method is used to explain the relationship between 
    # One continuous target variable (Y)
    # Two or more predictor X variables
    # Yhat = b0 + b1x1 + b2x2 + b3x3 + b4x4 where b0 = intercept X=0, b1 the coeff of x1, b2 the coeff of x2 and so on
    # If there are only two variables we can visualize the values  like say, Yhat = 1 + 2x1 + 3x2, where x1 and x2 can be visualized on a 2d plane

    lm = LinearRegression()
    
    # Fitting a Multiple Linear Model Estimator
    # We can extract the four predictor variables and store them in the variable Z
    Z = dfWithHeaders[["horsepower", "curb-weight", "engine-size", "highway-mpg"]]
    # Train the model 
    lm.fit(Z, dfWithHeaders["price"])    
    Yhat = lm.predict(X)
    # Find the Intercept
    print(lm.intercept) #b0
    # Find the coefficients
    print(lm.coeff) # gives an array with four elements (b1, b2, b3 and b4)
    # The estimated linear model 
    return

def ModelDevelopment():
    global graphs, dfCogAutos
    #Get DataFrame and Clean Numeric Data
    dataframer = DataFramer()
    charter = Charter()
    htmlHelper = HTMLHelper()
    #info = dataframer.DataFrameInfo(dfCogAutos)
    #dfInfos.append(info)

    dfNumCleaned = dfCogAutos.copy(deep=True)
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "price", coltype = "int64")
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "engine-size", coltype = "int64")
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "highway-mpg", coltype = "int64")
    dfNumCleaned = dataframer.CleanNumericColumn(dfData = dfNumCleaned, col = "peak-rpm", coltype = "int64")

    # In this section, we will develop several models that will predict the price of the car using the variables or features. 
    # This is just an estimate but should give us an objective idea of how much the car should cost.
    # Some questions we want to ask in this module
    # do I know if the dealer is offering fair value for my trade-in?
    # do I know if I put a fair value on my car?
    # Data Analytics, we often use Model Development to help us predict future observations from the data we have.
    # A Model will help us understand the exact relationship between different variables and how these variables are used to predict the result.

    #Linear Regression
    #One example of a Data Model that we will be using is

    #Simple Linear Regression. 
    #Simple Linear Regression is a method to help us understand the relationship between two variables:

    #The predictor/independent variable (X)
    #The response/dependent variable (that we want to predict)(Y)
    #The result of Linear Regression is a linear function that predicts the response (dependent) variable as a function of the predictor (independent) variable.

    #𝑌:𝑅𝑒𝑠𝑝𝑜𝑛𝑠𝑒 𝑉𝑎𝑟𝑖𝑎𝑏𝑙𝑒𝑋:𝑃𝑟𝑒𝑑𝑖𝑐𝑡𝑜𝑟 𝑉𝑎𝑟𝑖𝑎𝑏𝑙𝑒𝑠
    #Linear function:
    #𝑌ℎ𝑎𝑡=𝑎+𝑏𝑋
 
    #a refers to the intercept of the regression line0, in other words: the value of Y when X is 0
    #b refers to the slope of the regression line, in other words: the value with which Y changes when X increases by 1 unit
    #Lets load the modules for linear regression

    lm = LinearRegression()
    #How could Highway-mpg help us predict car price?
    #For this example, we want to look at how highway-mpg can help us predict car price. Using simple linear regression, we will create a linear function with "highway-mpg" as the predictor variable and the "price" as the response variable.
    X = dfNumCleaned[["highway-mpg"]]
    Y = dfNumCleaned["price"]
    #Fit the linear model using highway-mpg
    lm.fit(X,Y)
    # We can output a prediction
    Yhat=lm.predict(X)
    Yhat[0:5]   
    #What is the value of the intercept (a)?
    print(str(lm.intercept_))
    #What is the value of the slope (b)?
    print(str(lm.coef_))

    #What is the final estimated linear model we get?
    #As we saw above, we should get a final linear model with the structure:
    #𝑌ℎ𝑎𝑡=𝑎+𝑏𝑋
    #Plugging in the actual values we get:
    #price = 38423.31 - 821.73 x highway-mpg

    #Lab
    #Train the model using 'engine-size' as the independent variable and 'price' as the dependent variable?
    # Write your code below and press Shift+Enter to execute 
    lm1 = LinearRegression()
    X1=dfNumCleaned[["engine-size"]]
    Y1=dfNumCleaned[["price"]]
    lm1.fit(X1,Y1)
    print(str(lm1.intercept_))
    print(str(lm1.coef_))
    #What is the equation of the predicted line. You can use x and yhat or 'engine-size' or 'price'?
    print("Equation is: price = " + str(lm1.intercept_) + " + " + str(lm1.coef_) + " * engine-size")

    #What if we want to predict car price using more than one variable?
    #If we want to use more variables in our model to predict car price, we can use Multiple Linear Regression. Multiple Linear Regression is very similar to Simple Linear Regression, 
    #but this method is used to explain the relationship between one continuous response (dependent) variable and two or more predictor (independent) variables. 
    #Most of the real-world regression models involve multiple predictors. We will illustrate the structure by using four predictor variables, but these results can generalize to any integer:
    #𝑌:𝑅𝑒𝑠𝑝𝑜𝑛𝑠𝑒 𝑉𝑎𝑟𝑖𝑎𝑏𝑙𝑒𝑋1:𝑃𝑟𝑒𝑑𝑖𝑐𝑡𝑜𝑟 𝑉𝑎𝑟𝑖𝑎𝑏𝑙𝑒 1𝑋2:𝑃𝑟𝑒𝑑𝑖𝑐𝑡𝑜𝑟 𝑉𝑎𝑟𝑖𝑎𝑏𝑙𝑒 2𝑋3:𝑃𝑟𝑒𝑑𝑖𝑐𝑡𝑜𝑟 𝑉𝑎𝑟𝑖𝑎𝑏𝑙𝑒 3𝑋4:𝑃𝑟𝑒𝑑𝑖𝑐𝑡𝑜𝑟 𝑉𝑎𝑟𝑖𝑎𝑏𝑙𝑒 4
    #𝑎:𝑖𝑛𝑡𝑒𝑟𝑐𝑒𝑝𝑡𝑏1:𝑐𝑜𝑒𝑓𝑓𝑖𝑐𝑖𝑒𝑛𝑡𝑠 𝑜𝑓 𝑉𝑎𝑟𝑖𝑎𝑏𝑙𝑒 1𝑏2:𝑐𝑜𝑒𝑓𝑓𝑖𝑐𝑖𝑒𝑛𝑡𝑠 𝑜𝑓 𝑉𝑎𝑟𝑖𝑎𝑏𝑙𝑒 2𝑏3:𝑐𝑜𝑒𝑓𝑓𝑖𝑐𝑖𝑒𝑛𝑡𝑠 𝑜𝑓 𝑉𝑎𝑟𝑖𝑎𝑏𝑙𝑒 3𝑏4:𝑐𝑜𝑒𝑓𝑓𝑖𝑐𝑖𝑒𝑛𝑡𝑠 𝑜𝑓 𝑉𝑎𝑟𝑖𝑎𝑏𝑙𝑒 4
    #The equation is given by
    #𝑌ℎ𝑎𝑡=𝑎+𝑏1𝑋1+𝑏2𝑋2+𝑏3𝑋3+𝑏4𝑋4
 
    #From the previous section we know that other good predictors of price could be:
    # Horsepower Curb-weight Engine-size Highway-mpg
    #Let's develop a model using these variables as the predictor variables.
    lmz = LinearRegression()
    Z = dfNumCleaned[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']]
    #Fit the linear model using the four above-mentioned variables.
    lmz.fit(Z, dfNumCleaned['price'])
    print(str(lmz.intercept_))
    print(str(lmz.coef_))
    # What is the final estimated linear model that we get?
    # As we saw above, we should get a final linear function with the structure:
    # 𝑌ℎ𝑎𝑡=𝑎+𝑏1𝑋1+𝑏2𝑋2+𝑏3𝑋3+𝑏4𝑋4
    # What is the linear function we get in this example?
    #Price = -15678.742628061467 + 52.65851272 x horsepower + 4.69878948 x curb-weight + 81.95906216 x engine-size + 33.58258185 x highway-mpg

    #Create and train a Multiple Linear Regression model "lm2" where the response variable is price, 
    #and the predictor variable is 'normalized-losses' and 'highway-mpg'.
    lmx = LinearRegression()
    N = dfNumCleaned[["normalized-losses", "highway-mpg"]]
    lmx.fit(N, dfNumCleaned[["price"]])
    print(str(lmx.intercept_))
    print(str(lmx.coef_))

    # Model Evaluation using Visualization
    # Now that we've developed some models, how do we evaluate our models and how do we choose the best one? One way to do this is by using visualization.

    # Regression Plot
    # When it comes to simple linear regression, an excellent way to visualize the fit of our model is by using regression plots.
    # This plot will show a combination of a scattered data points (a scatter plot), as well as the fitted linear regression line going through the data. 
    # This will give us a reasonable estimate of the relationship between the two variables, the strength of the correlation, as well as the direction (positive or negative correlation).
    # Let's visualize Horsepower as potential predictor variable of price:
    reg1 = charter.RegPlot(xaxis="highway-mpg", yaxis="price", dfData=dfNumCleaned, imgformat="png")
    graphs.append(reg1)
    # We can see from this plot that price is negatively correlated to highway-mpg, since the regression slope is negative. 
    # One thing to keep in mind when looking at a regression plot is to pay attention to how scattered the data points are around the regression line. 
    # This will give you a good indication of the variance of the data, and whether a linear model would be the best fit or not. 
    # If the data is too far off from the line, this linear model might not be the best model for this data. Let's compare this plot to the regression plot of "peak-rpm".
    reg2 = charter.RegPlot(xaxis="peak-rpm", yaxis="price", dfData=dfNumCleaned, imgformat="png")
    graphs.append(reg2)
    # Comparing the regression plot of "peak-rpm" and "highway-mpg" we see that the points for "highway-mpg" are much closer to the generated line and on the average decrease. 
    # The points for "peak-rpm" have more spread around the predicted line, and it is much harder to determine if the points are decreasing or increasing as the "highway-mpg" increases.

    # Given the regression plots above is "peak-rpm" or "highway-mpg" more strongly correlated with "price". Use the method ".corr()" to verify your answer.
    dfCorr = dfNumCleaned[["peak-rpm","highway-mpg","price"]].corr()
    dfTable = htmlHelper.GetHTMLTableFromDataFrame(dfCorr, None, True)
    dfName = "Correlation between peak-rpm, highway-mpg and price"
    dfTables.append((dfName, dfTable))

    # Residual Plot
    # A good way to visualize the variance of the data is to use a residual plot.
    # What is a residual?
    # The difference between the observed value (y) and the predicted value (Yhat) is called the residual (e). When we look at a regression plot, the residual is the distance from the data point to the fitted regression line.
    # So what is a residual plot?
    # A residual plot is a graph that shows the residuals on the vertical y-axis and the independent variable on the horizontal x-axis.
    # What do we pay attention to when looking at a residual plot?
    # We look at the spread of the residuals:
    # If the points in a residual plot are randomly spread out around the x-axis, then a linear model is appropriate for the data. Why is that? Randomly spread out residuals means that the variance is constant, and thus the linear model is a good fit for this data.
    res1 = charter.ResidPlot(xaxis="highway-mpg", yaxis="price", dfData=dfNumCleaned, imgformat="png")
    graphs.append(res1)

    res2 = charter.ResidPlot(xaxis="peak-rpm", yaxis="price", dfData=dfNumCleaned, imgformat="png")
    graphs.append(res2)
    #What is this plot telling us?
    #We can see from this residual plot that the residuals are not randomly spread around the x-axis, which leads us to believe that maybe a non-linear model is more appropriate for this data.

    # Multiple Linear Regression
    # How do we visualize a model for Multiple Linear Regression? This gets a bit more complicated because you can't visualize it with regression or residual plot.
    # One way to look at the fit of the model is by looking at the distribution plot: 
    # We can look at the distribution of the fitted values that result from the model and compare it to the distribution of the actual values.
    # First lets make a prediction
    mlm = LinearRegression()
    ytarget = "price"
    mlm.fit(Z, dfNumCleaned[ytarget])
    Yhat = mlm.predict(Z)
    dist1 = charter.DistPlot(yhat = Yhat, ytarget = "price", charttitle="Actual vs Fitted Values for Price", distlabel="Fitted Values", xlabel="Price (in dollars)", ylabel="Proportion of Cars", axlabel="Actual Value", dfData=dfNumCleaned, imgformat="png")
    graphs.append(dist1)
    # We can see that the fitted values are reasonably close to the actual values, since the two distributions overlap a bit. However, there is definitely some room for improvement.
    return

def PolynomialRegression():
    # Polynomial Regression and Pipelines
    # Polynomial regression is a particular case of the general linear regression model or multiple linear regression models.
    # We get non-linear relationships by squaring or setting higher-order terms of the predictor variables.
    # There are different orders of polynomial regression:
    # Quadratic - 2nd order
    # 𝑌ℎ𝑎𝑡=𝑎+𝑏1𝑋2+𝑏2𝑋2
    # Cubic - 3rd order
    #𝑌ℎ𝑎𝑡=𝑎+𝑏1𝑋2+𝑏2𝑋2+𝑏3𝑋3
    #Higher order:
    #𝑌=𝑎+𝑏1𝑋2+𝑏2𝑋2+𝑏3𝑋3....
    # We saw earlier that a linear model did not provide the best fit while using highway-mpg as the predictor variable. Let's see if we can try fitting a polynomial model to the data instead.

    # We will use the following function to plot the data:

    # lets get the variables
    #x = df['highway-mpg']
    #y = df['price']
    # Let's fit the polynomial using the function polyfit, then use the function poly1d to display the polynomial function.

    # Here we use a polynomial of the 3rd order (cubic) 
    #f = np.polyfit(x, y, 3)
    #p = np.poly1d(f)
    #print(p)
    # Let's plot the function

    #poly1 = charter.PolyPlot(p,x,y,"highway-mpg")
    #np.polyfit(x, y, 3)
    # We can already see from plotting that this polynomial model performs better than the linear model. This is because the generated polynomial function "hits" more of the data points.

    #Question #4:
    #Create 11 order polynomial model with the variables x and y from above? ​
    #Double-click here for the solution.

    #The analytical expression for Multivariate Polynomial function gets complicated. For example, the expression for a second-order (degree=2)polynomial with two variables is given by:
    # 𝑌ℎ𝑎𝑡=𝑎+𝑏1𝑋1+𝑏2𝑋2+𝑏3𝑋1𝑋2+𝑏4𝑋21+𝑏5𝑋22
    #We can perform a polynomial transform on multiple features. First, we import the module:

    #from sklearn.preprocessing import PolynomialFeatures
    #We create a PolynomialFeatures object of degree 2:
    #pr=PolynomialFeatures(degree=2)
    #Z_pr=pr.fit_transform(Z)
    #The original data is of 201 samples and 4 features
    #print(Z.shape)
    #after the transformation, there 201 samples and 15 features
    #print(Z_pr.shape)
    
    # Pipeline
    # Data Pipelines simplify the steps of processing the data. We use the module Pipeline to create a pipeline. We also use StandardScaler as a step in our pipeline.

    #from sklearn.pipeline import Pipeline
    #from sklearn.preprocessing import StandardScaler
    #We create the pipeline, by creating a list of tuples including the name of the model or estimator and its corresponding constructor.
    #Input=[('scale',StandardScaler()), ('polynomial', PolynomialFeatures(include_bias=False)), ('model',LinearRegression())]
    #we input the list as an argument to the pipeline constructor
    #pipe=Pipeline(Input)
    #print(pipe)
    #We can normalize the data, perform a transform and fit the model simultaneously.
    #pipe.fit(Z,y)
    #Similarly, we can normalize the data, perform a transform and produce a prediction simultaneously
    #ypipe=pipe.predict(Z)
    #print(ypipe[0:4])
    #Question #5:
    #Create a pipeline that Standardizes the data, then perform prediction using a linear regression model using the features Z and targets y
    #Write your code below and press Shift+Enter to execute 
    #Double-click here for the solution.
    return