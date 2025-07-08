from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
from app.graphql.context import Context

# async def custom_context_getter(request):
#     return Context(request)

graphql_router = GraphQLRouter(
    schema,
    # graphiql=False,
    # context_getter=lambda request: {"request": request}
)

app = FastAPI()

@app.middleware("http")
async def db_session_middleware(request, call_next):
    from app.core.database import db
    request.state.db = db
    response = await call_next(request)
    return response

app.include_router(graphql_router, prefix="/api/graphql")
