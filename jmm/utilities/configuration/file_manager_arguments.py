from pydantic import BaseModel
from pydantic import StrictStr

from jmm.utilities.file_manager import Mode

class FileManagerArguments(BaseModel):
    mode: Mode
    file_path_pattern: StrictStr
