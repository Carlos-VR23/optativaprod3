# app/repositories/restaurant_repository.py
from google.cloud.firestore_v1.base_query import FieldFilter
from app.core.firebase import db

class RestaurantRepository:
    def __init__(self):
        self.collection = db.collection("restaurants")

    def create(self, data: dict) -> dict:
        ref = self.collection.document()
        data["id"] = ref.id
        data["avgRating"] = 0
        data["numRatings"] = 0
        ref.set(data)
        return data

    def get(self, restaurant_id: str):
        doc = self.collection.document(restaurant_id).get()
        if not doc.exists:
            return None
        return doc.to_dict() | {"id": doc.id}

    def list(self, category: str | None = None, city: str | None = None, price: int | None = None, order_by: str = "name", limit: int = 20, start_after: str | None = None):
        query = self.collection
        if category:
            query = query.where(filter=FieldFilter("category", "==", category))
        if city:
            query = query.where(filter=FieldFilter("city", "==", city))
        if price:
            query = query.where(filter=FieldFilter("price", "==", price))
        
        query = query.order_by(order_by).limit(limit)
        
        if start_after:
            last_doc = self.collection.document(start_after).get()
            if last_doc.exists:
                query = query.start_after(last_doc)
                
        return [doc.to_dict() | {"id": doc.id} for doc in query.stream()]

    def update(self, restaurant_id: str, data: dict) -> dict | None:
        ref = self.collection.document(restaurant_id)
        doc = ref.get()
        if not doc.exists:
            return None
        ref.update(data)
        return self.get(restaurant_id)

    def delete(self, restaurant_id: str) -> bool:
        ref = self.collection.document(restaurant_id)
        doc = ref.get()
        if not doc.exists:
            return False
        ref.delete()
        return True