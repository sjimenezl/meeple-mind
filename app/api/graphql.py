from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema

graphql_router = GraphQLRouter(schema)

graphql_app = APIRouter()
graphql_app.include_router(graphql_router, prefix="/graphql")
