import threading
import time
from fastapi import FastAPI, HTTPException, UploadFile, File
from contextlib import asynccontextmanager
from pydantic import BaseModel


active_messages = []

# 2. Define the Background Task
def printer_loop():
    """
    Runs in the background. Checks the message list every 60 seconds.
    """
    while True:
        print("--- Ticking ---")
        
        if not active_messages:
            # Default behavior if list is empty
            print("hi")
        else:
            # Print all active messages in order
            for msg in active_messages:
                print(msg)
        
        # Wait for 60 seconds
        time.sleep(5)

# 3. Start the Background Thread on App Startup


@asynccontextmanager
async def lifespan(app: FastAPI):
    # daemon=True ensures this thread dies when the main server is stopped
    printer_thread = threading.Thread(target=printer_loop, daemon=True)
    printer_thread.start()
    yield


# 1. Initialize the App and State
app = FastAPI(lifespan=lifespan)


# 4. Define Data Models for the API
class Message(BaseModel):
    text: str


# 5. Define API Endpoints
@app.get("/")
def read_root():
    return {"status": "running", "current_messages": active_messages}

# @app.get("/word")
# def add_message():
#     """Adds a string to the print list."""
#     return {"status": "got", "list": active_messages}


@app.post("/script")
def add_Script(uploaded_file: UploadFile = File(...)):
    file_location = f"./scripts/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    return {"Result": "OK"}


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