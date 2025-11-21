from pydantic import BaseModel
from datetime import datetime,timedelta


class NewScript(BaseModel):
    name: str
    description: str = ""
    active : bool = True

    mainCode : str
    triggerCode : str = ""


    firstCall : datetime = datetime.now()
    delta: timedelta = timedelta(seconds=5)
    forceRun: bool = False