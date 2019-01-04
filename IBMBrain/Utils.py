import pandas as pd
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

class HTMLHelper:
    DefaultTableClasses = "table table-striped table-bordered table-condensed table-responsive"
    def GetHTMLTableFromDataFrame(self, df, styleclasses = None):     
        dfTable = None
        if df is not None:
            if styleclasses is None:
                dfTable = df.to_html(header="true", classes = self.DefaultTableClasses, index = False)
            else:
                dfTable = df.to_html(header="true", classes = styleclasses, index = False)
        return dfTable