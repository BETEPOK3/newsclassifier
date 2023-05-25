from datetime import datetime

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from fastapi import FastAPI, Request, status, Form, Body, Depends
from pydantic import BaseModel, Field

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
    article_categories: list
    article_keywords: list
    article_date: datetime
    article_text: str


class ArticlesRequestSchema(BaseModel):
    category: int = Field(default=-1)
    sort_by: str = Field(default=None)
    search_text: str = Field(default=None)
    page: int = Field(default=0)
    page_size: int = Field(default=10)


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
async def get_article_list(request: Request, search_params: ArticlesRequestSchema = Depends()):
    try:
        content = dict()
        articles = await queries.get_article_list(search_params.page, search_params.page_size,
                                          {
                                              "category": search_params.category,
                                              "sort_by": search_params.sort_by,
                                              "search_text": search_params.search_text
                                          })
        accept_header = request.headers.get('accept')
        if accept_header == "application/json":
            for article in articles["articles"]:
                date_str = article["article_date"].isoformat()
                article["article_date"] = date_str
            return JSONResponse(articles)
        content["articles"] = articles["articles"]
        content["cur_page"] = search_params.page
        content["articles_count"] = articles["articles_count"]
        content["categories"] = await get_categories()
        return templates.TemplateResponse("pages/articles_list.html",
                                          {"request": request, "content": content},
                                          status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)
        return get_error_page(request, e)


@app.get("/article", response_class=HTMLResponse)
async def get_article_page(request: Request, article_id: int):
    try:
        content = dict()
        article = await get_article(article_id)
        content["article"] = article
        accept_header = request.headers.get('accept')
        if accept_header == "application/json":
            date_str = article["article_date"].isoformat()
            article["article_date"] = date_str
            return JSONResponse(content["article"])
        return templates.TemplateResponse("pages/article_text.html",
                                          {"request": request, "content": content},
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
