from datetime import datetime,timedelta
from .requests import NewScript
import importlib

class Script():
    id = None
    name = ""
    description = ""

    isactive = True
    lastCall = None
    callNumbers = 0

    main = None
    trigger = None


    activationDateTime = None
    delta = None
    data = {}
    forceRun = False

    def __init__(self,id,ScriptData: NewScript):
        self.id = id
        self.name = ScriptData.name
        self.description = ScriptData.description
        self.isactive = ScriptData.active
        self.activationDateTime = ScriptData.firstCall

        self.delta = ScriptData.delta
        self.forceRun = ScriptData.forceRun

        if ScriptData.triggerCode == None or ScriptData.triggerCode == "":
            
            self.trigger = self.timeTrigger
            forceRun = runFirst

        else:
            self.trigger = self.getTrigger()
            
        self.main = self.getMainFunction() 

    def getMainFunction(self):
        module = importlib.import_module(f".scripts.{self.id}.main",package=__package__)
        return module.main

    def getTrigger(self):
        module = importlib.import_module(f".scripts.{self.id}.trigger",package=__package__)
        return module.trigger

 
    
    def call(self):

        if self.trigger(self.data) or forceRun:
            self.forceRun = False
            self.main(self.data)
            self.callNumbers += 1
            self.lastCall = datetime.today()

    def timeTrigger(self,data):
        return True

  
    
