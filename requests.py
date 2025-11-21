from pydantic import BaseModel
from datetime import datetime,timedelta


class NewScript(BaseModel):
    name: str
    description: str = ""
    active : bool = True

    triggerCode : str = "def trigger(data):\n\treturn True"
    mainCode : str = "def main(data):\n\tprint(\"default\")"


    firstCall : datetime = datetime.now()
    delta: timedelta = timedelta(seconds=5)
    forceRun: bool = False


