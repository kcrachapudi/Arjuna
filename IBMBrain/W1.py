# Data Acquisition
import pandas as pd
import Utils
from Utils import *

FileURL = "https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data"
LocalPath = "../Data/"
FileName = "OriginalAutosData85.csv"
FileType = "csv"
SaveLocal = True

#Autos Dataframes
dfWithHeaders = None
dfWithoutPrice = None

def ProcessAutosData():
    global FileURL, LocalPath, FileName, FileType, SaveLocal, dfWithHeaders, dfWithoutPrice
    print("Hi from W1")
    filereader = FileReader(LocalPath, FileName, FileType, FileURL, str(SaveLocal))
    dfOriginalAutos = filereader.ReadFile()
    DissectAutosData(dfOriginalAutos)
    return

def DissectAutosData(dfOriginal):
    global FileURL, LocalPath, FileName, FileType, SaveLocal, dfWithHeaders, dfWithoutPrice
    #Show the first 5 rows of df
    #print(dfOriginal.head(5))

    #Show the last 10 rows of df
    #print(dfOriginal.tail(10))

    #create headers list
    originalAutosHeaders = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
            "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
            "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
            "peak-rpm","city-mpg","highway-mpg","price"]
    
    #assign headers
    dfOriginal.columns = originalAutosHeaders
    #copy df to new df
    dfWithHeaders = dfOriginal.copy(deep=True)
    filereader = FileReader(LocalPath,"AutosData85Headers.csv", FileType, None, str(SaveLocal))
    filereader.SaveLocalFile(dfWithHeaders)
    #now the head shold show the new header
    #print(dfWithHeaders.head(5))

    #Drop missing values along the column 'price    
    dfWithoutPrice = dfWithHeaders.copy(deep=True)
    dfWithoutPrice.dropna(subset=["price"], axis=0)
    filereader = FileReader(LocalPath,"AutosData85WithoutPrice.csv", FileType, None, str(SaveLocal))
    filereader.SaveLocalFile(dfWithoutPrice)

    return

def OtherDataFrameCommands():
    return