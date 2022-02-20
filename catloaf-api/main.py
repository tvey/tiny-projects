from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from utils import get_image

app = FastAPI()


@app.get('/catloaf')
def get_catloaf():
    image_bytes = get_image()
    return StreamingResponse(image_bytes)
