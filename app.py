from fastapi import FastAPI, HTTPException
import uvicorn
import requests
from pydantic import BaseModel, validator
from typing import List

class UserDataModel(BaseModel):
    name: str
    email: str
    first_name: str
    last_name: str
    password: str
    friend: List[str]

    @validator('email')
    def email_must_contain_at_symbol(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v

user_json_data = []

app = FastAPI()

@app.get("/")
async def hello() -> dict[str, str]:
    data = {"Hello": "World"}
    return data

@app.get("/ping")
def ping() -> str:
    return f"This is just a sample data"

@app.post("/user")
async def create_user(user: UserDataModel):
    if user.email in [u.email for u in user_json_data]:
        raise HTTPException(status_code=400, detail="Email already exists")
    user_json_data.append(user)
    return user

@app.get("/users")
def get_users():
    return user_json_data

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)