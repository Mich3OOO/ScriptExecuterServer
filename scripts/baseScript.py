from datetime import datetime,timedelta

class baseScript():
    id = None
    name = ""
    description = ""
    isactive = True
    lastCall = None
    callNumbers = 0

    main = None
    hasToRun = None


    firstCall = None
    delta = None
    data = {}
    forceRun = False

    # custom
    def __init__(self,mainFunction: function,hasToRunFunction: function, forceRun: bool = False):
        main = mainFunction
        hasToRun = hasToRunFunction
        self.forceRun = forceRun

    # ever n time
    def __init__(self, mainFunction: function, deltaTime:timedelta,runFirst: bool, start = None):
        if start == None and runFirst:
            firstCall = datetime.today()
        elif start == None and not runFirst:
            firstCall = datetime.today() + deltaTime
        else:
            firstCall = start
        
        main = mainFunction
        hasToRun = self.hasToRunEvery
        forceRun = runFirst
    
    def call(self):

        if hasToRun(data) or forceRun:
            forceRun = False
            self.main(data)
            callNumbers += 1
            lastCall = datetime.today()

            if firstCall == None:
                firstCall = datetime.today()

    def hasToRunEvery(self,data):
        r = False
        if datetime.today() - firstCall >= delta:
            r = True
        else:
            r = False

        return r
  
    
   
class timeTrigeredScript(baseScript):
    pass

class onTimeTrigeredScript(baseScript):
    pass