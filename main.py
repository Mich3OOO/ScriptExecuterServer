import threading
import time
from fastapi import FastAPI, HTTPException, UploadFile, File
from contextlib import asynccontextmanager
from .requests import NewScript
import uuid
from .baseScript import Script
from datetime import datetime,timedelta
import os


active_scripts = []

# 2. Define the Background Task
def runner():
    
    while True:
        # print("--- Ticking ---")
        
        for script in active_scripts:
            
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

@app.get("/script")
def add_message():
    return {"status": "got", "list": active_scripts}


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
        
    
    active_scripts.append(Script(id,ScriptData))

    

    return id



# @app.delete("/word")
# def remove_message(message: Message):
#     """Removes the first occurrence of the string from the list."""
#     if message.text in active_messages:
#         active_messages.remove(message.text)
#         return {"status": "removed", "message": message.text, "list": active_messages}
#     else:
#         raise HTTPException(status_code=404, detail="String not found in list")

# @app.delete("/")
# def clear_all():
#     """Clears all messages, reverting to printing 'hi'."""
#     active_messages.clear()
#     return {"status": "cleared", "list": active_messages}