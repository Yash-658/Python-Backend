from fastapi import FastAPI
from app.routers import problems

app = FastAPI()
app.include_router(problems.router)      # without this, FastAPI doesn't know that the routes inside problems.py should be part of the application.

@app.get("/")
async def root():
    return {'message':'hello doll'}