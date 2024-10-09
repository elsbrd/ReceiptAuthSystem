import uvicorn
from fastapi import FastAPI

from src.api.routes import auth_routes, receipt_routes

app = FastAPI()


def include_api_router(router, prefix: str, tags: list):
    app.include_router(router, prefix=f"/api{prefix}", tags=tags)


include_api_router(auth_routes.router, prefix="/auth", tags=["auth"])
include_api_router(receipt_routes.router, prefix="", tags=["receipts"])


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
