from fastapi import FastAPI
from .routers import hello

app = FastAPI()
app.include_router(hello.router)


@app.get('/')
def index():
    return {'message': 'Hello!'}
