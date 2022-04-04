from pydantic import BaseModel
from pydantic import StrictStr

class FileManagerArguments(BaseModel):
    mode: StrictStr
    file_path_pattern: StrictStr
