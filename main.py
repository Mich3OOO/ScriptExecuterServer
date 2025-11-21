import threading
import time
from fastapi import FastAPI, HTTPException, UploadFile, File
from contextlib import asynccontextmanager
from .requests import NewScript
import uuid
from .baseScript import Script
from datetime import datetime,timedelta
import os
import shutil

active_scripts = {}

# 2. Define the Background Task
def runner():
    
    while True:
        # print("--- Ticking ---")
        
        for script in active_scripts.copy().values():
            
            if script.lastCall == None or (script.isactive and  datetime.now() - script.lastCall >= script.delta):
                script.call()

        # time.sleep(5)


        

# 3. Start the Background Thread on App Startup


@asynccontextmanager
async def lifespan(app: FastAPI):
    runner_thread = threading.Thread(target=runner, daemon=True)
    runner_thread.start()
    yield


# 1. Initialize the App and State
app = FastAPI(lifespan=lifespan)


# 5. Define API Endpoints
@app.get("/")
def read_root():
    return {"status": "running"}

@app.get("/script/")
def add_message():
    return active_scripts

@app.get("/script/{script_id}")
def add_message(script_id: uuid.UUID):
    if script_id in active_scripts.keys():
        return active_scripts[script_id]
    else:
        raise HTTPException(status_code=404, detail="Script not found")

@app.post("/script")
def add_Script(ScriptData: NewScript):

    id = uuid.uuid4()

    
    os.makedirs(os.path.dirname(f"./scripts/{id}/"))

    with open(f"./scripts/{id}/main.py","w+") as pyFile:
        pyFile.write(ScriptData.mainCode)

    open(f"./scripts/{id}/__init__.py","w+").close()

    if ScriptData.triggerCode != None and ScriptData.triggerCode != "":
        with open(f"./scripts/{id}/trigger.py","w+") as pyFile:
           pyFile.write(ScriptData.triggerCode)
        
    
    active_scripts[id] = Script(id,ScriptData)

    return id



@app.delete("/script/{script_id}")
def remove_message(script_id: uuid.UUID):
    if script_id in active_scripts.keys():
        shutil.rmtree(f"./scripts/{script_id}/")
        return active_scripts.pop(script_id)
    else:
        raise HTTPException(status_code=404, detail="Script not found")
