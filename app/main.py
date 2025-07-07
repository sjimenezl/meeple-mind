from fastapi import FastAPI
from app.api.graphql import graphql_app
from app.core.config import settings

app = FastAPI()

@app.middleware("http")
async def db_session_middleware(request, call_next):
    from app.core.database import db

    request.state.db = db
    response = await call_next(request)
    return response

# montas GraphQL en la ruta /graphql
app.include_router(graphql_app, prefix="/api")

for route in app.routes:
    print(route.path)
