from datetime import timedelta
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from quizzy.auth import (ACCESS_TOKEN_EXPIRE_MINUTES, Token, User,
                         authenticate_user, create_access_token, fake_users_db,
                         get_current_active_user)
from quizzy.config import settings
from quizzy.openai import get_pet_names, get_quiz

app = FastAPI()


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


templates = Jinja2Templates(directory="quizzy/templates")
app.mount("/static", StaticFiles(directory="quizzy/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def index(request: Request, animal: str = Form(...)):
    result = get_pet_names(animal)
    return templates.TemplateResponse(
        "index.html", {"request": request, "result": result}
    )


class Question(BaseModel):
    question: str
    options: list[str]
    answer: str


class Response(BaseModel):
    quiz: list[Question]


@app.get("/quiz/", response_model=Response)
async def quiz(topic: str, level: str, age: str):
    result = get_quiz(topic, level, age)
    return result


if __name__ == "__main__":
    uvicorn.run("quizzy.app:app", host="localhost", port=5001, reload=True)
