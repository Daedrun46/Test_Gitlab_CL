from sqlalchemy import Column, Integer, String, Text

from database import Base


class Recipe(Base):
    """
    Модель рецепта для базы данных.

    Поля:
    - id: Уникальный идентификатор рецепта.
    - title: Название рецепта.
    - cooking_time: Время приготовления в минутах.
    - ingredients: Список ингредиентов в виде строки (разделитель - запятая).
    - description: Текстовое описание рецепта, инструкции по приготовлению.
    - views: Счётчик просмотров рецепта,
      используется для сортировки по популярности.
    """

    __tablename__ = "recipes"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Уникальный идентификатор рецепта",
    )
    title = Column(String(255), nullable=False, doc="Название рецепта")
    cooking_time = Column(
        Integer, nullable=False, doc="Время приготовления в минутах"
    )
    ingredients = Column(
        Text, nullable=False, doc="Список ингредиентов, через запятую"
    )
    description = Column(
        Text, nullable=False, doc="Подробная инструкция по приготовлению"
    )
    views = Column(Integer, default=0, doc="Количество просмотров рецепта")
