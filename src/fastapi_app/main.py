from fastapi import FastAPI

from .router import exchanges, outlets, processors


app = FastAPI()

app.include_router(outlets.router)
app.include_router(processors.router)
app.include_router(exchanges.router)

