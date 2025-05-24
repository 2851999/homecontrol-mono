from fastapi import FastAPI, Request
from homecontrol_auth.routers.users import users
from homecontrol_base_api.exceptions import BaseAPIError, handle_base_api_error

app = FastAPI()

app.include_router(users)

app.add_exception_handler(BaseAPIError, handle_base_api_error)


@app.get("/")
async def root():
    return {"message": "Hello World"}
