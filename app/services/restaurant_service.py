# app/services/restaurant_service.py
from fastapi import HTTPException
from app.repositories.restaurant_repository import RestaurantRepository
from app.domain.schemas import RestaurantCreate, RestaurantUpdate

class RestaurantService:
    def __init__(self):
        self.repository = RestaurantRepository()

    def create(self, payload: RestaurantCreate) -> dict:
        return self.repository.create(payload.model_dump())

    def get(self, restaurant_id: str) -> dict:
        restaurant = self.repository.get(restaurant_id)
        if restaurant is None:
            raise HTTPException(status_code=404, detail="Restaurante no encontrado")
        return restaurant

    def list(self, category: str | None = None, city: str | None = None, price: int | None = None, order_by: str = "name", limit: int = 20, start_after: str | None = None):
        return self.repository.list(
            category=category,
            city=city,
            price=price,
            order_by=order_by,
            limit=limit,
            start_after=start_after
        )

    def update(self, restaurant_id: str, payload: RestaurantUpdate) -> dict:
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        restaurant = self.repository.update(restaurant_id, data)
        if restaurant is None:
            raise HTTPException(status_code=404, detail="Restaurante no encontrado")
        return restaurant

    def delete(self, restaurant_id: str) -> None:
        deleted = self.repository.delete(restaurant_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Restaurante no encontrado")