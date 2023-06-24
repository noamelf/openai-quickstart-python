import openai
from pydantic import BaseModel

import uvicorn

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from quizzy.config import settings
from quizzy.openai import get_pet_names, get_quiz


app = FastAPI()
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
