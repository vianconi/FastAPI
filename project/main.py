from fastapi import FastAPI


app = FastAPI(title='App reseña de peliculas',
              description='Proyecto capaz de reseñar peliculas',
              version='1')


@app.get('/')
async def index():
    return 'Hello world!'
