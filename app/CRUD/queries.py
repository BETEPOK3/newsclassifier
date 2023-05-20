from app.models.basic_models import *
from database import database
from sqlalchemy import select, insert, delete, update, or_, and_, func
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


async def create_article(article):
    try:
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
            if (resultCategory is None):
                query = (
                    insert(Category).values(category_name=category)
                )
                resultCategory = await database.fetch_one(query)
            query = (
                insert(ArticleCategory).values(article_id=resultArticle.article_id,
                                               category_id=resultCategory.category_id)
            )
            await database.fetch_one(query)
        return resultArticle.article_id
    except Exception as e:
        logger.error(e)
