from sqlalchemy import MetaData, Integer, String, Column, Date, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base()


class Article(Base):
    __tablename__ = 'article'
    metadata = metadata
    id_article = Column(Integer(), primary_key=True, autoincrement=True)
    article_authors = Column(ARRAY(String))
    article_keywords = Column(ARRAY(String))
    article_date = Column(Date(), nullable=False)
    article_text = Column(String(), nullable=False)


class Category(Base):
    __tablename__ = 'category'
    metadata = metadata
    id_category = Column(Integer(), primary_key=True, autoincrement=True)
    category_name = Column(String(), unique=True, nullable=False)


class ArticleCategory(Base):
    __tablename__ = 'article_category'
    metadata = metadata
    id_article_category = Column(Integer(), primary_key=True, autoincrement=True)
    id_article = Column(ForeignKey("article.id_article", onupdate="RESTRICT", ondelete="RESTRICT"))
    id_category = Column(ForeignKey("category.id_category", onupdate="RESTRICT", ondelete="RESTRICT"))
