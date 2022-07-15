import inspect, os, datetime, json

def dictToStr(jsonData):
    return json.dumps(jsonData, ensure_ascii=False, indent=4)

def saveToFile(txt, to, mode="w"):
    file = open(to, mode, encoding="utf8")
    file.write(txt)
    file.close()

def saveObjToFile(to, *texts, mode="w"):
    file = open(to, mode, encoding="utf8")
    for text in texts:
        text = dictToStr(text)
        file.write(text)
        file.write("\n")
    file.close()

#
# Class logging introduce easy way to fast tail log place in the script
#
# log include next information:
#   timestamp - time when logging method is called
#   log type - INFO, ERROR
#   constant text - it is set once, but logging always
#   file name - name of a file wherein logging method is called
#   line - number of line in the file
#   function/method - wherein logging method is called
#   log text - string with whom logging function is called
#       
# Class Parameters: 
#   mainText    : str,   not mandatory,   default: "" 
#   enPrinting  : bool,  not mandatory,   default: True 
#   enSave      : bool,  not mandatory,   default: True 
#   path        : str,   not mandatory,   default: "logFile.log"
#
# Control:
#   INFO(text) logging method, prints or saves (depends of EN_CLI and EN_FILE parameters) text with other parameters 
#       if text parameter is miss, "Enter" string will be printed/saved by default
#   INFO(text) logging method, prints and saves logs with other parameters
#   EN_CLI vasiables is responsible for printing logs on a terminal
#       True means printing (default)
#       False means not printing 
#   EN_FILE vasiables is responsible for saving logs on a log file
#       True means saving (default)
#       False means not saving 
# 
# Example use:
#   log = logging("ConstText")
#   log.INFO()
#   log.INFO("example text")
# Result:
#   2022-07-15 14.45.52.094981	INFO::ConstText::fileName.py::29	>>funcName	::Enter
#   2022-07-15 14.45.52.094981	INFO::ConstText::fileName.py::29	>>funcName	::example text
#
class logging:
    def __init__(self, mainText:str="", enPrinting:bool=True, enSave:bool=True, path:str="logFile.log"):
        self.EN_CLI:bool    = enPrinting
        self.EN_FILE:bool   = enSave
        self.__mainText     = mainText
        self.__path         = path
        self.__inspLevel    = 1

    # Print or save Info log or do nothing
    def INFO(self, txt="Enter"):
        if self.EN_CLI or self.EN_FILE:
            inspectionData = inspect.stack()
            self.__prepareLog("INFO", txt, inspectionData, False)
    
    # Print & save Error log
    def ERROR(self, txt=""):
        if self.EN_CLI or self.EN_FILE:
            inspectionData = inspect.stack()
            self.__prepareLog("ERROR", txt, inspectionData, True)
    
    # Preparation of log string
    def __prepareLog(self, type, txt, inspectionData, force=True):
        
        # Get timestamp, basic log building
        time   = str(datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S.%f"))
        logTxt = time + "\t" + type + "::" + self.__mainText

        # Get file name from which logging methot is called
        filePath = inspectionData[self.__inspLevel].filename
        file     = os.path.basename(filePath)#[ : file.rfind(".") ]
        logTxt  += "::" + file

        # Get line number from logging methot is called
        line = str(inspectionData[self.__inspLevel].lineno)
        logTxt  += "::" + line

        # Get function name from which logging methot is called
        func = inspectionData[self.__inspLevel].function
        if func == "<module>": func = file
        logTxt += "\t>>" + func
        
        # Add log text
        logTxt += "\t::" + txt
        
        # Print on terminal
        if self.EN_CLI or force: print(logTxt)
        
        # Save to logfile
        if self.EN_FILE or force: 
            logFile = open(self.__path, mode="a", encoding="utf8")
            logFile.write(logTxt + "\n")
            logFile.close()
