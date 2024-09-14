from fastapi import FastAPI
import homecontrol_base_api

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
