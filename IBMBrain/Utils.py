import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from pandas.compat import StringIO

class DataFramer():
    def __init__(self):
        pass

    def DataFrameInfo(self, dfData = None):
        info = ""
        if(dfData is None):
            dfData = pd.DataFrame(np.random.randn(100, 3), columns =['A', 'B', 'C'])
        a = StringIO()
        dfData.info(buf = a)  
        # Example to convert to html
        contents = a.getvalue().split('\n')
        for lines in contents:
            info = info + "<pre>" + lines + "</pre>"
        return info

    def CleanNumericColumn(self, dfData, col, coltype = None):
        if(coltype is None):
            coltype = "int64"

        #cleanup the col column by converting any ? to 0
        dfData[col].replace('?', 0, inplace = True)
        #Convert the col column from object to numeric
        dfData[col] = pd.to_numeric(dfData[col], "coerce")
        #Convert any NaN values that were coerced to 0
        dfData[col].replace(np.nan, 0, inplace = True)
        if(coltype == "int" or coltype == "Integer" or coltype == "int64" ):
            #Ensure that the col column is integer
            dfData[col] = dfData[col].astype(coltype)

        return dfData

class FileProcessor:
    LocalPath = ""
    FileName = ""
    FileURL = ""
    FileType = ""
    SaveLocal = None

    def __init__(self, localpath, filename, filetype, fileurl = None, savelocal = None):
        self.LocalPath = localpath
        self.FileName = filename
        self.FileType = filetype
        self.FileURL = fileurl
        self.SaveLocal = savelocal
        return

    def ReadFile(self):
        print("Read File")
        dfResult = self.ReadLocalFile()
        if(dfResult is None and self.FileURL is not None):
            dfResult = self.ReadURLFile()
        return dfResult
    
    def ReadLocalFile(self):
        try:
            dfLocalFile = pd.read_csv(self.LocalPath+self.FileName)
        except Exception as ex:
            print("Error in reading Local File " + self.LocalPath + self.FileName + str(ex))
            dfLocalFile = None
        return dfLocalFile

    def ReadURLFile(self):
        #Read the Online File provided by the URL and assign it to the variable
        try:
            dfURLFile = pd.read_csv(self.FileURL, header=None)
            if(self.SaveLocal):
                try:
                    dfURLFile.to_csv(self.LocalPath+self.FileName, index = False)
                except:
                    pass
        except:
            dfURLFile = None
        return dfURLFile

    def SaveLocalFile(self, dfData):
        try:
            dfData.to_csv(self.LocalPath+self.FileName, index = False)
        except:
            pass
        return

class Charter:
    def BuildGraph(self, x_coordinates, y_coordinates, type="png"):
        img = io.BytesIO()
        plt.plot(x_coordinates, y_coordinates)
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return 'data:image/png;base64,{}'.format(graph_url)

    def BoxPlot(self, xaxis = None, dfData = None, imgformat="png"):
        img = io.BytesIO()
        #sns.boxplot(x=xaxis, y=yaxis, data=dfData)
        plt.boxplot(dfData[xaxis])
        plt.savefig(img, format = imgformat)
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return 'data:image/png;base64,{}'.format(graph_url)

    def BoxPlot2(self, xaxis = None, yaxis = None, dfData = None, imgformat="png"):
        img = io.BytesIO()
        sns.boxplot(x=xaxis, y = yaxis, data=dfData)
        plt.savefig(img, format = imgformat)
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return 'data:image/png;base64,{}'.format(graph_url)

    def ScatterPlot(self, xaxis, yaxis, dfData, imgformat="png"):
        img = io.BytesIO()
        #required conversion to float as there is a call to np.sqrt internally that can only handle floats
        dfData[xaxis] = dfData[xaxis].astype("float")
        dfData[yaxis] = dfData[yaxis].astype("float")
        plt.scatter(dfData[xaxis], dfData[yaxis])
        plt.title("Scatter Plot of " + xaxis + " vs " + yaxis)
        plt.xlabel(xaxis)
        plt.ylabel(yaxis)
        plt.savefig(img, format = imgformat)
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return 'data:image/png;base64,{}'.format(graph_url)

    def HeatMap(self, dfData = None, imgformat="png"):
        img = io.BytesIO()
        plt.pcolor(dfData, cmap = "RdBu")
        plt.colorbar()
        plt.savefig(img, format = imgformat)
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return 'data:image/png;base64,{}'.format(graph_url)

    def HeatMapSNS(self, dfData = None, imgformat="png"):
        img = io.BytesIO()
        g = sns.heatmap(dfData, cmap="RdBu", cbar=True)
        #The set_facecolor is optional and use it to set empty values 
        g.set_facecolor("black")
        plt.savefig(img, format = imgformat)
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return 'data:image/png;base64,{}'.format(graph_url)

class HTMLHelper:
    DefaultTableClasses = "table table-striped table-bordered table-condensed table-responsive"
    def GetHTMLTableFromDataFrame(self, df, styleclasses = None, indexer = False):     
        dfTable = None
        if df is not None:
            if styleclasses is None:
                dfTable = df.to_html(header="true", classes = self.DefaultTableClasses, index = indexer)
            else:
                dfTable = df.to_html(header="true", classes = styleclasses, index = indexer)
        return dfTable

    def AddMarkup(htmlString):
        return 