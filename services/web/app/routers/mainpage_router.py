from datetime import date

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from fastapi import FastAPI, Request, status, Form, Body, Depends
from pydantic import BaseModel, Field
from typing import List, Optional

from services.web.app.CRUD import queries
from services.web.app.CRUD.queries import *
from services.web import database
from fastapi.staticfiles import StaticFiles
from services.web.logger.custom_logging import CustomizeLogger
from pathlib import Path

import grpc
from schema123.gen.types_pb2 import CategoryPrediction
from schema123.gen.categories_pb2 import PredictCategoriesRequest, PredictCategoriesResponse
from schema123.gen.categories_pb2_grpc import CategoriesStub

templates = Jinja2Templates(directory="app/templates")


class ArticleSchema(BaseModel):
    article_title: str
    article_author: str = Field(default=None)
    article_categories: List[str]
    article_keywords: List[str] = Field(default=[])
    article_date: Optional[date] = None
    article_text: str


class ArticlesRequestSchema(BaseModel):
    category: int = Field(default=-1)
    sort_by: str = Field(default=None)
    search_text: str = Field(default=None)
    page: int = Field(default=0)


def get_error_page(request, exc):
    content = dict()
    content["error"] = exc
    return templates.TemplateResponse("pages/error_page.html",
                                      {"request": request, "content": content},
                                      status_code=status.HTTP_400_BAD_REQUEST)


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
        page_size = 10
        articles = await queries.get_article_list(search_params.page, page_size,
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
        return get_error_page(request, Exception("Неверный article_id"))


@app.get("/article/create", response_class=HTMLResponse)
async def create_article(request: Request):
    try:
        categories = await queries.get_all_categories()
        content = {"categories": categories}
        return templates.TemplateResponse("pages/article_create.html",
                                          {"request": request, "content": content},
                                          status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)
        return get_error_page(request, e)


@app.post("/article/create")
async def create_article(request: Request, article: ArticleSchema):
    try:
        if (len(article.article_categories) == 0):
            raise Exception("Количество категорий не может быть равно нулю")
        if article.article_date is None:
            article.article_date = datetime.now().date()

        article_id = await queries.create_article(article)
        if article_id is None:
            raise Exception("id статьи == null (из-за попытки создания новой категории)")
        accept = request.headers["accept"]
        if (accept == "application/json"):
            return {"id": article_id}
        return RedirectResponse("/article/{}".format(article_id),
                                status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        logger.error(e)
        return get_error_page(request, e)


@app.delete("/article/{article_id}")
async def delete_article(request: Request, article_id: int):
    try:
        await queries.delete_article(article_id)
        accept = request.headers["accept"]
        if (accept == "application/json"):
            return {"id": article_id}
        return RedirectResponse("/index", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        logger.error(e)
        return get_error_page(request, e)


@app.get("/article/update/{article_id}", response_class=HTMLResponse)
async def update_article(request: Request, article_id: int):
    try:
        content = dict()
        article = await get_article(article_id)
        content["article"] = article
        accept_header = request.headers.get('accept')
        if accept_header == "application/json":
            date_str = article["article_date"].isoformat()
            article["article_date"] = date_str
            return JSONResponse(content["article"])
        content["keywords"] = ";".join(article["article_keywords"])
        content["all_categories"] = await queries.get_all_categories()
        content["categories"] = [dct["category_name"] for dct in article["categories"]]
        return templates.TemplateResponse("pages/article_update.html",
                                          {"request": request, "content": content},
                                          status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)
        return get_error_page(request, e)


@app.post("/article/update/{article_id}")
async def update_article(request: Request, article_id: int, params: dict):
    try:
        content = dict()
        if params["article_date"] is None:
            params["article_date"] = datetime.now().date().isoformat()
        if len(params["article_categories"]) == 0:
            raise Exception("Количество категорий не может быть равно нулю")
        article = await queries.update_article(article_id=article_id, params=params)
        content["article"] = article
        accept_header = request.headers.get("accept")
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


@app.get("/article/predict", response_class=HTMLResponse)
async def predict_article(request: Request):
    try:
        return templates.TemplateResponse("pages/article_predict.html",
                                          {"request": request},
                                          status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)
        return get_error_page(request, e)


@app.post("/article/predict", response_class=JSONResponse)
async def predict_article(request: Request, article_text: dict):
    try:
        with grpc.insecure_channel("classifier:8035") as channel:
            stub = CategoriesStub(channel)
            response: PredictCategoriesResponse = stub.PredictCategories(PredictCategoriesRequest(text=article_text["article_text"]))
            result = list(filter(lambda x: (x.prediction >= 0.5), response.result))

            if len(result) == 0:
                max_prediction = max(response.result, key=lambda x: x.prediction)
                if max_prediction.prediction < 0.01:
                    return {"categories123": "Категории для данного текста не были распознаны."}
                result.append(max_prediction)

            return {"categories123": '\n'.join(["{}: {:.2f}".format(x.category, x.prediction) for x in result])}

    except Exception as e:
        logger.error(e)
        return get_error_page(request, e)
