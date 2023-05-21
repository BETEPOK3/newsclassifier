from sqlalchemy import MetaData, Integer, String, Column, Date, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base()


class Article(Base):
    __tablename__ = 'article'
    metadata = metadata
    article_id = Column(Integer(), primary_key=True, autoincrement=True)
    article_title = Column(String(), nullable=False)
    article_author = Column(String())
    article_keywords = Column(ARRAY(String))
    article_date = Column(Date(), nullable=False)
    article_text = Column(String(), nullable=False)


class Category(Base):
    __tablename__ = 'category'
    metadata = metadata
    category_id = Column(Integer(), primary_key=True, autoincrement=True)
    category_name = Column(String(), unique=True, nullable=False)


class ArticleCategory(Base):
    __tablename__ = 'article_category'
    metadata = metadata
    article_category_id = Column(Integer(), primary_key=True, autoincrement=True)
    article_id = Column(ForeignKey("article.article_id", onupdate="RESTRICT", ondelete="RESTRICT"))
    category_id = Column(ForeignKey("category.category_id", onupdate="RESTRICT", ondelete="RESTRICT"))
