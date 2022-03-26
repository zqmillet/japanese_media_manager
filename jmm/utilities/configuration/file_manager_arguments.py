from pydantic import BaseModel
from pydantic import StrictStr

class FileManagerArguments(BaseModel):
    mode: StrictStr
    destination_directory: StrictStr
