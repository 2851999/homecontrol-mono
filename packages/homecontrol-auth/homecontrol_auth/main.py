from fastapi import FastAPI
from homecontrol_auth.routers.users import users

app = FastAPI()

app.include_router(users)


@app.get("/")
async def root():
    return {"message": "Hello World"}
