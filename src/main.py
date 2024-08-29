from fastapi import FastAPI
from src.routers import menu_item, order, report

app = FastAPI()

# register routes
app.include_router(menu_item.router)
app.include_router(order.router)
app.include_router(report.router)
