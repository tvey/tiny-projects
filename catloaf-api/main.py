from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from utils import get_image

app = FastAPI()


@app.get('/')
async def get_catloaf():
    image_bytes = await get_image()
    return StreamingResponse(image_bytes)
