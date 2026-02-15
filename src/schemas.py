from typing import List

from pydantic import BaseModel, Field


class RecipeListItem(BaseModel):
    """
    Схема для отображения краткой информации о рецепте (для списка).
    """

    id: int = Field(..., description="Уникальный идентификатор рецепта")
    title: str = Field(..., description="Название рецепта")
    cooking_time: int = Field(
        ..., description="Время приготовления в минутах"
    )
    views: int = Field(..., description="Количество просмотров рецепта")


class RecipeDetail(BaseModel):
    """
    Схема для детальной информации о рецепте.
    """

    id: int = Field(..., description="Уникальный идентификатор рецепта")
    title: str = Field(..., description="Название рецепта")
    cooking_time: int = Field(
        ..., description="Время приготовления в минутах"
    )
    ingredients: List[str] = Field(..., description="Список ингредиентов")
    description: str = Field(
        ..., description="Подробная инструкция по приготовлению"
    )
    views: int = Field(..., description="Количество просмотров рецепта")


class RecipeCreate(BaseModel):
    """
    Схема для создания нового рецепта через POST запрос.
    """

    title: str = Field(..., description="Название рецепта")
    cooking_time: int = Field(
        ..., description="Время приготовления в минутах"
    )
    ingredients: List[str] = Field(..., description="Список ингредиентов")
    description: str = Field(
        ..., description="Подробная инструкция по приготовлению"
    )
