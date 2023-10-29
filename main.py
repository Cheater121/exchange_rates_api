import uvicorn
from fastapi import FastAPI

from app.api.routers.routers import all_routers

app = FastAPI(
    title="Currency Exchange Rates API"
)

for router in all_routers:
    app.include_router(router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Currency Exchange Rates API server"}


# if __name__ == "__main__":
#     uvicorn.run(app="main:app", reload=True)
