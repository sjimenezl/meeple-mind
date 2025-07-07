from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
from app.graphql.context import Context

def custom_context_getter(request):
    if request.method == "POST":
        return Context(request)
    return None

graphql_router = GraphQLRouter(
    schema,
    context_getter=custom_context_getter
)

graphql_app = APIRouter()
graphql_app.include_router(graphql_router, prefix="/graphql")
