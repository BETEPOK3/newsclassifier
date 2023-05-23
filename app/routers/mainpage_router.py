from datetime import date

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi import FastAPI, Request, status, Form, Body
from pydantic import BaseModel, Field
from typing import List

from app.CRUD import queries
from app.CRUD.queries import *
import database
from fastapi.staticfiles import StaticFiles
from logger.custom_logging import CustomizeLogger
from pathlib import Path

templates = Jinja2Templates(directory="app/templates")


class ArticleSchema(BaseModel):
    article_title: str
    article_author: str = Field(default=None)
    article_categories: List[str]
    article_keywords: List[str] = Field(default=[])
    article_date: date
    article_text: str

    class Config:
        orm_mode = True


def get_error_page(request, exc):
    content = dict()
    content["error"] = exc
    return templates.TemplateResponse("pages/error_page.html", {"request": request, "content": content})


exceptions = {
    404: get_error_page
}

config_path = Path(Path(__file__).parents[2], "logger", "logging_config.json")


def create_app() -> FastAPI:
    _app = FastAPI(exception_handlers=exceptions)
    _logger = CustomizeLogger.make_logger(config_path)
    _app.logger = _logger
    return _app


app = create_app()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
async def startup():
    await database.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()


@app.get("/", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
async def get_index(request: Request):
    try:
        content = dict()
        content["data_list"] = await get_all_data()
        return templates.TemplateResponse("pages/index.html",
                                          {"request": request, "content": content},
                                          status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)
        return get_error_page(request, e)


@app.get("/article/create", response_class=HTMLResponse)
async def create_article(request: Request):
    try:
        return templates.TemplateResponse("pages/article_create.html",
                                          {"request": request},
                                          status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)
        return get_error_page(request, e)


@app.post("/article/create", response_class=HTMLResponse)
async def create_article(request: Request, article: ArticleSchema):
    try:
        articleId = await queries.create_article(article)
        return "Article with id: {} created successfully!".format(articleId)
    except Exception as e:
        logger.error(e)
        return get_error_page(request, e)


@app.delete("/article/{articleId}", status_code=status.HTTP_200_OK)
async def delete_article(request: Request, articleId: int):
    try:
        await queries.delete_article(articleId)
        return "Article with id: {} deleted successfully!".format(articleId)
    except Exception as e:
        logger.error(e)
        return get_error_page(request, e)
