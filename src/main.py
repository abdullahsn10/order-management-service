from fastapi import FastAPI
from src.routers import menu_item

app = FastAPI()

# register routes
app.include_router(menu_item.router)
