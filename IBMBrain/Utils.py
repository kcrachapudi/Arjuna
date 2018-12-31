import pandas as pd
class FileReader:
    LocalPath = ""
    FileName = ""
    FileURL = ""
    FileType = ""
    SaveLocal = None

    def __init__(self, localpath, filename, filetype, fileurl, savelocal):
        self.LocalPath = localpath
        self.FileName = filename
        self.FileType = filetype
        self.FileURL = fileurl
        self.SaveLocal = savelocal
        return

    def ReadFile(self):
        print("Read File")
        dfResult = self.ReadLocalFile()
        if(dfResult is None):
            dfResult = self.ReadURLFile()
        return dfResult
    
    def ReadLocalFile(self):
        try:
            dfLocalFile = pd.read_csv(self.LocalPath+self.FileName, index = False)
        except:
            dfLocalFile = None
        return dfLocalFile

    def ReadURLFile(self):
        #Read the Online File provided by the URL and assign it to the variable
        try:
            dfURLFile = pd.read_csv(self.FileURL, header=None)
            if(self.SaveLocal):
                try:
                    dfURLFile.to_csv(self.LocalPath+self.FileName)
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
