from fastapi import FastAPI
from src.routers import menu_item, order, report
from src.settings.settings import OPENAPI_URL, ROOT_PATH

app = FastAPI(
    openapi_url=OPENAPI_URL,
    root_path=ROOT_PATH,
)


# register routes
app.include_router(menu_item.router)
app.include_router(order.router)
app.include_router(report.router)
