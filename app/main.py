from fastapi import FastAPI
from app.api.graphql import graphql_app

app = FastAPI()

# montas GraphQL en la ruta /graphql
app.include_router(graphql_app, prefix="/api")

for route in app.routes:
    print(route.path)
