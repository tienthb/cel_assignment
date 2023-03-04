from typing import Union
from fastapi import FastAPI, File, UploadFile
import pandas as pd
import io
import json
import uvicorn

from .router import outlets, processors


app = FastAPI()

app.include_router(outlets.router)
app.include_router(processors.router)


