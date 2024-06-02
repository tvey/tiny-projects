from fastapi import FastAPI

from src.router import curr_router

app = FastAPI()
app.include_router(curr_router)
