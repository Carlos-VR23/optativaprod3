# app/api/v1/restaurants.py
from fastapi import APIRouter, Query
from app.services.restaurant_service import RestaurantService
from app.domain.schemas import RestaurantCreate, RestaurantUpdate

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])
service = RestaurantService()

@router.get("")
async def list_restaurants(
    category: str | None = None,
    city: str | None = None,
    price: int | None = Query(default=None, ge=1, le=3),
    order_by: str = "name",
    limit: int = Query(default=20, ge=1, le=100),
    start_after: str | None = None
):
    return service.list(
        category=category,
        city=city,
        price=price,
        order_by=order_by,
        limit=limit,
        start_after=start_after
    )

@router.get("/{restaurant_id}")
async def get_restaurant(restaurant_id: str):
    return service.get(restaurant_id)

@router.post("", status_code=201)
async def create_restaurant(payload: RestaurantCreate):
    return service.create(payload)

@router.patch("/{restaurant_id}")
async def update_restaurant(restaurant_id: str, payload: RestaurantUpdate):
    return service.update(restaurant_id, payload)

@router.delete("/{restaurant_id}", status_code=204)
async def delete_restaurant(restaurant_id: str):
    service.delete(restaurant_id)