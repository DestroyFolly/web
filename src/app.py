from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from User.handler import user_router
from Trainer.handler import trainer_router
from Train.handler import train_router
from Gym.handler import gym_router
from Muscles.handler import muscle_router
import json
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

# Подключаем API-маршруты
app.include_router(user_router)
app.include_router(trainer_router)
app.include_router(train_router)
app.include_router(gym_router)
app.include_router(muscle_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Замените на список допустимых доменов, например ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все HTTP-методы
    allow_headers=["*"],  # Разрешить все заголовки
)

# Генерация OpenAPI схемы и сохранение в файл swagger.json при старте приложения
@app.on_event("startup")
async def generate_openapi():
    with open("swagger.json", "w") as f:
        json.dump(app.openapi(), f)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/admin/")
async def open_admin_page():
    return RedirectResponse(url="http://127.0.0.1:56543")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)


