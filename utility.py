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


class logging:
    def __init__(self, mainText = "", enPrinting=True, enSave=True, path="logFile.log"):
        self.__mainText     = mainText
        self.EN_CLI         = enPrinting
        self.EN_FILE        = enSave
        self.__path         = path
        self.__inspLevel    = 1

    def INFO(self, txt="Enter to func"):
        if self.EN_CLI or self.EN_FILE:
            inspectionData = inspect.stack()
            self.__prepareLog("INFO", txt, inspectionData, False)
    
    def ERROR(self, txt=""):
        if self.EN_CLI or self.EN_FILE:
            inspectionData = inspect.stack()
            self.__prepareLog("ERROR", txt, inspectionData, False)

    def __prepareLog(self, type, txt, inspectionData, force=True):
        
        time   = str(datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S.%f"))
        logTxt = time + "\t" + type + "::" + self.__mainText

        filePath = inspectionData[self.__inspLevel].filename
        file     = os.path.basename(filePath)
        # file     = file[ : file.rfind(".") ]
        logTxt  += "::" + file

        line = str(inspectionData[self.__inspLevel].lineno)
        logTxt  += "::" + line

        func = inspectionData[self.__inspLevel].function
        if func == "<module>": func = file
        logTxt += "\t>>" + func
        
        logTxt += "\t::" + txt
        
        # Print on terminal
        if self.EN_CLI or force: print(logTxt)
        
        # Save to logfile
        if self.EN_FILE or force: 
            logFile = open("logFile.log", mode="a", encoding="utf8")
            logFile.write(logTxt + "\n")
            logFile.close()
