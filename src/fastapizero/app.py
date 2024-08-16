from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/batatinha')
def read_batatinha():
    return {'batatinha': 'batatinha'}
