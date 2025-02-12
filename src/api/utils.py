from typing import Annotated
from fastapi import Path


TypeID = Annotated[int, Path(gt=0, lt=2147483647)]
