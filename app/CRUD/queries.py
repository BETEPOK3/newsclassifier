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
            ).where(Article.id_article == data_id)
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
