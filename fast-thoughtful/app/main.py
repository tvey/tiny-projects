from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def index():
    return {
        'thought': (
            'Peace cannot be kept by force; '
            'it can only be achieved by understanding.'
        )
    }
