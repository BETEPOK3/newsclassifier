from datetime import datetime
from databases.backends.postgres import Record
from services.web.app.models.basic_models import *
from services.web.database import database
from sqlalchemy import select, insert, delete, update, or_, and_, func, desc
import logging

logger = logging.getLogger(__name__)


async def get_data(data_id):
    try:
        query = (
            select(
                [
                    Article
                ]
            ).where(Article.article_id == data_id)
        )
        data = await database.fetch_one(query)
        return data
    except Exception as e:
        logger.error(e)


async def get_all_categories():
    try:
        query = (
            select(
                [
                    Category
                ]
            )
        )
        categories = await database.fetch_all(query)
        return categories
    except Exception as e:
        logger.error(e)


async def get_all_data():
    try:
        query = (
            select(
                [
                    Article
                ]
            )
        )
        data = await database.fetch_all(query)
        return data
    except Exception as e:
        logger.error(e)


async def insert_data(data):
    try:
        query = (
            insert(Article).values(data=data)
        )
        data = await database.fetch_one(query)
        return data.id
    except Exception as e:
        logger.error(e)


async def get_categories():
    try:
        query = (
            select(
                [
                    Category
                ]
            ).order_by(Category.category_name)
        )
        categories = await database.fetch_all(query)
        return categories
    except Exception as e:
        logger.error(e)


def article_record_to_dict(article, categories):
    article_dict = {}
    for key in article._mapping.keys():
        article_dict[key] = article._mapping[key]
    article_dict["categories"] = []
    for cat in categories:
        cat_dict = {}
        for key in cat._mapping.keys():
            if key != "article_id":
                cat_dict[key] = cat._mapping[key]
        article_dict["categories"].append(cat_dict)
    return article_dict


async def get_article_list(page: int, page_size: int, params: dict):
    try:
        offset = page * page_size
        subquery = select(func.count(Article.article_id)
                          )
        query = (
            select(
                [
                    Article
                ]
            )
        )
        sort_by = params["sort_by"]
        if sort_by == "title":
            query = query.order_by(Article.article_title, desc(Article.article_id))
        elif sort_by == "date":
            query = query.order_by(desc(Article.article_date), desc(Article.article_id))
        elif sort_by == "author":
            query = query.order_by(Article.article_author, desc(Article.article_id))
        category = params["category"]
        if category != -1:
            query = query.filter(ArticleCategory.article_id == Article.article_id,
                                 Category.category_id == ArticleCategory.category_id,
                                 Category.category_id == category)
            subquery = subquery.filter(ArticleCategory.article_id == Article.article_id,
                                       Category.category_id == ArticleCategory.category_id,
                                       Category.category_id == category)
        search_text = params["search_text"]
        if search_text not in [None, ""]:
            query = query.filter(or_(
                Article.article_author.ilike(f"%{search_text}%"),

                Article.article_title.ilike(f"%{search_text}%")
            ))
            subquery = subquery.filter(or_(
                Article.article_author.ilike(f"%{search_text}%"),

                Article.article_title.ilike(f"%{search_text}%")
            ))
        count = await database.fetch_one(subquery)
        query = query.offset(offset).limit(page_size)
        articles = await database.fetch_all(query)
        articles_ids = [a.article_id for a in articles]
        query = (
            select(
                [
                    Category,
                    ArticleCategory.article_id
                ]
            )
            .where(ArticleCategory.article_id.in_(articles_ids), Category.category_id == ArticleCategory.category_id)
        )
        categories = await database.fetch_all(query)
        res_list = []
        for article in articles:
            article_categories = [cat for cat in categories if cat.article_id == article.article_id]
            article_dict = article_record_to_dict(article, article_categories)
            res_list.append(article_dict)
        return {"articles": res_list, "articles_count": count.count_1}
    except Exception as e:
        logger.error(e)


async def get_article(article_id):
    try:
        query = (
            select(
                [
                    Article
                ]
            )
            .where(Article.article_id == article_id)
        )
        article = await database.fetch_one(query)
        query = (
            select(
                [
                    Category
                ]
            )
            .where(ArticleCategory.article_id == article_id, Category.category_id == ArticleCategory.category_id)
        )
        categories = await database.fetch_all(query)
        article_dict = article_record_to_dict(article, categories)
        return article_dict
    except Exception as e:
        logger.error(e)


async def create_article(article):
    try:
        async with database.transaction():
            query = (
                insert(Article).values(article_title=article.article_title,
                                       article_author=article.article_author,
                                       article_keywords=article.article_keywords,
                                       article_date=article.article_date,
                                       article_text=article.article_text
                                       )
            )
            resultArticle = await database.fetch_one(query)
            for category in article.article_categories:
                query = (select(Category.category_id).where(Category.category_name == category))
                resultCategory = await database.fetch_one(query)
                if resultCategory is None:
                    raise Exception("Нельзя добавить новую категорию при создании статьи.\n"
                                    "Необходимо указать уже существующую")
                query = (
                    insert(ArticleCategory).values(article_id=resultArticle.article_id,
                                                   category_id=resultCategory.category_id)
                )
                await database.fetch_one(query)
            return resultArticle.article_id
    except Exception as e:
        logger.error(e)


async def delete_article(article_id):
    try:
        query = (
            delete(Article).where(Article.article_id == article_id)
        )
        await database.fetch_one(query)
        return article_id
    except Exception as e:
        logger.error(e)


def check_article_none(article: Record, params: dict) -> Article:
    new_article = Article()

    new_article.article_id = article.get("article_id")

    if params.get("article_title") is not None:
        new_article.article_title = params.get("article_title")
    else:
        new_article.article_title = article.get("article_title")

    if params.get("article_author") is not None:
        new_article.article_author = params.get("article_author")
    else:
        new_article.article_author = article.get("article_author")

    if params.get("article_keywords") is not None:
        new_article.article_keywords = params.get("article_keywords")
    else:
        new_article.article_keywords = article.get("article_keywords")

    if params.get("article_date") is not None:
        date_str = params.get("article_date")
        date = datetime.strptime(date_str, "%Y-%m-%d")
        new_article.article_date = date
    else:
        date_str = article.get("article_date")
        date = datetime.strptime(date_str, "%Y-%m-%d")
        new_article.article_date = date

    if params.get("article_text") is not None:
        new_article.article_text = params.get("article_text")
    else:
        new_article.article_text = article.get("article_text")

    return new_article


async def select_article_for_update(article_id: int) -> Record:
    query = (
        select(Article).where(Article.article_id == article_id)
    )
    result_article = await database.fetch_one(query)
    return result_article


async def select_categories_for_update(article_id: int) -> Record:
    query = (
        select([Category])
        .where(ArticleCategory.article_id == article_id, Category.category_id == ArticleCategory.category_id)
    )
    result_categories = await database.fetch_all(query)
    return result_categories


async def update_article(article_id: int, params: dict):
    try:
        article = await select_article_for_update(article_id=article_id)
        new_article = check_article_none(article=article, params=params)
        query = (
            update(Article).where(Article.article_id == article_id).values(
                article_title=new_article.article_title,
                article_author=new_article.article_author,
                article_keywords=new_article.article_keywords,
                article_date=new_article.article_date,
                article_text=new_article.article_text
            )
        )
        await database.fetch_one(query)
        result_article = await select_article_for_update(article_id=article_id)
        categories = await select_categories_for_update(article_id=article_id)

        new_categories = params.get("article_categories")

        query = (
            delete(ArticleCategory).where(ArticleCategory.article_id == article_id)
        )
        await database.fetch_one(query)

        if new_categories is None:
            article_dict = article_record_to_dict(result_article, categories)
            return article_dict
        else:
            result_categories = []
            for new_category in new_categories:
                query = (select(Category).where(Category.category_name == new_category))
                category = await database.fetch_one(query)

                if category is None:
                    raise Exception("Нельзя добавить новую категорию при обновлении статьи.\n"
                                    "Необходимо указать уже существующую")
                else:
                    result_categories.append(category)

                query = (insert(ArticleCategory).values(article_id=result_article.article_id,
                                                        category_id=category.get("category_id")))
                await database.fetch_one(query)

        article_dict = article_record_to_dict(result_article, result_categories)
        return article_dict

    except Exception as e:
        logger.error(e)
