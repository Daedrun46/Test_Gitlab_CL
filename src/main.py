import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select, desc
from contextlib import asynccontextmanager

from database import get_db, init_db
from models import Recipe
from schemas import RecipeCreate, RecipeListItem, RecipeDetail

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="Cookbook API",
    description="API сервиса кулинарной книги",
    version="1.0.0",
    lifespan=lifespan,
)



@app.get(
    "/recipes",
    response_model=list[RecipeListItem],
    summary="Получить список рецептов",
    description=(
        "Возвращает список всех рецептов, отсортированных по популярности "
        "(количество просмотров), а затем по времени готовки."
    ),
)
async def get_recipes(db: AsyncSession = Depends(get_db)):
    stmt = select(Recipe).order_by(desc(Recipe.views), Recipe.cooking_time)
    result = await db.execute(stmt)
    recipes = result.scalars().all()
    return recipes


@app.get(
    "/recipes/{recipe_id}",
    response_model=RecipeDetail,
    summary="Получить рецепт",
    description="Возвращает детальную информацию о рецепте и увеличивает счётчик просмотров.",
)
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    recipe = await db.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe.views += 1
    await db.commit()
    await db.refresh(recipe)

    return RecipeDetail(
        id=recipe.id,
        title=recipe.title,
        cooking_time=recipe.cooking_time,
        ingredients=recipe.ingredients.split(", "),
        description=recipe.description,
        views=recipe.views,
    )


@app.post(
    "/recipes",
    response_model=RecipeDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Создать рецепт",
    description="Создаёт новый рецепт в базе данных.",
)
async def create_recipe(
    recipe: RecipeCreate,
    db: AsyncSession = Depends(get_db),
):
    db_recipe = Recipe(
        title=recipe.title,
        cooking_time=recipe.cooking_time,
        ingredients=", ".join(recipe.ingredients),
        description=recipe.description,
    )

    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)

    return RecipeDetail(
        id=db_recipe.id,
        title=db_recipe.title,
        cooking_time=db_recipe.cooking_time,
        ingredients=recipe.ingredients,
        description=db_recipe.description,
        views=db_recipe.views,
    )
