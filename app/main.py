# app/main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.v1.restaurants import router as restaurants_router
from app.services.restaurant_service import RestaurantService

app = FastAPI(title="FriendlyEats FastAPI")

# API REST (JSON)
app.include_router(restaurants_router, prefix="/api/v1")

# Archivos estáticos (CSS, JS) y plantillas HTML
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

service = RestaurantService()

ORDER_OPTIONS = {"name": "Nombre (A-Z)", "avgRating": "Mejor calificados"}


@app.get("/health")
async def health():
    return {"status": "ok"}


# ---------- Vistas HTML ----------

@app.get("/")
async def home(
    request: Request,
    city: str | None = None,
    category: str | None = None,
    price: str | None = None,
    order_by: str = "name",
):
    # El <select> vacío manda "" -> lo tratamos como "sin filtro"
    city = city or None
    category = category or None
    price_int = int(price) if price and price.isdigit() and 1 <= int(price) <= 3 else None
    if order_by not in ORDER_OPTIONS:
        order_by = "name"

    # Valores disponibles para llenar los filtros
    everything = service.list(limit=100)
    cities = sorted({r["city"] for r in everything})
    categories = sorted({r["category"] for r in everything})

    restaurants = service.list(
        city=city, category=category, price=price_int,
        order_by=order_by, limit=100,
    )
    if order_by == "avgRating":
        restaurants.sort(key=lambda r: r.get("avgRating", 0), reverse=True)
    restaurants = restaurants[:20]  # límite inicial de 20

    return templates.TemplateResponse(
        request,
        "restaurants.html",
        {
            "restaurants": restaurants,
            "cities": cities,
            "categories": categories,
            "filters": {"city": city, "category": category, "price": price_int, "order_by": order_by},
            "order_options": ORDER_OPTIONS,
        },
    )


# IMPORTANTE: /restaurants/new debe ir ANTES de /restaurants/{restaurant_id}
@app.get("/restaurants/new")
async def new_restaurant_page(request: Request):
    return templates.TemplateResponse(
        request, "restaurant_form.html", {"restaurant": None}
    )


@app.get("/restaurants/{restaurant_id}")
async def restaurant_detail_page(request: Request, restaurant_id: str):
    restaurant = service.get(restaurant_id)  # lanza 404 si no existe
    return templates.TemplateResponse(
        request, "restaurant_detail.html", {"restaurant": restaurant}
    )


@app.get("/restaurants/{restaurant_id}/edit")
async def edit_restaurant_page(request: Request, restaurant_id: str):
    restaurant = service.get(restaurant_id)
    return templates.TemplateResponse(
        request, "restaurant_form.html", {"restaurant": restaurant}
    )
