# scripts/seed.py  ->  ejecutar con:  python -m scripts.seed
from app.core.firebase import db

U = "https://images.unsplash.com/"

restaurants = [
    {"name": "La Abuela", "category": "Mexicana", "city": "Puebla", "price": 2,
     "photoUrl": U + "photo-1552566626-52f8b828add9", "avgRating": 4.5, "numRatings": 20},
    {"name": "Pizza Central", "category": "Pizza", "city": "Puebla", "price": 1,
     "photoUrl": U + "photo-1513104890138-7c749659a591", "avgRating": 4.0, "numRatings": 12},
    {"name": "Sushi Kame", "category": "Japonesa", "city": "Puebla", "price": 3,
     "photoUrl": U + "photo-1579871494447-9811cf80d66c", "avgRating": 4.7, "numRatings": 31},
    {"name": "Tacos El Güero", "category": "Mexicana", "city": "Puebla", "price": 1,
     "photoUrl": U + "photo-1565299585323-38d6b0865b47", "avgRating": 4.3, "numRatings": 58},
    {"name": "Trattoria Roma", "category": "Italiana", "city": "Cholula", "price": 3,
     "photoUrl": U + "photo-1498579150354-977475b7ea0b", "avgRating": 4.6, "numRatings": 24},
    {"name": "Burger Lab", "category": "Hamburguesas", "city": "Puebla", "price": 2,
     "photoUrl": U + "photo-1568901346375-23c9450c58cd", "avgRating": 3.9, "numRatings": 40},
    {"name": "Café del Zócalo", "category": "Cafetería", "city": "Puebla", "price": 1,
     "photoUrl": U + "photo-1554118811-1e0d58224f24", "avgRating": 4.1, "numRatings": 17},
    {"name": "Mole Poblano Casa Real", "category": "Mexicana", "city": "Cholula", "price": 3,
     "photoUrl": U + "photo-1504674900247-0877df9cc836", "avgRating": 4.8, "numRatings": 45},
    {"name": "Green Bowl", "category": "Saludable", "city": "Atlixco", "price": 2,
     "photoUrl": U + "photo-1512621776951-a57141f2eefd", "avgRating": 4.2, "numRatings": 9},
    {"name": "Pizzería Napoli", "category": "Pizza", "city": "Cholula", "price": 2,
     "photoUrl": U + "photo-1574071318508-1cdbab80d002", "avgRating": 4.4, "numRatings": 28},
]

for restaurant in restaurants:
    db.collection("restaurants").add(restaurant)

print(f"Datos semilla creados: {len(restaurants)} restaurantes")
