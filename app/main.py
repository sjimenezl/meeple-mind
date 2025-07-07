from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
from app.graphql.context import Context

def custom_context_getter(request):
    return Context(request)


graphql_router = GraphQLRouter(
    schema,
    graphiql=False,
    context_getter=custom_context_getter
)

app = FastAPI()

@app.middleware("http")
async def db_session_middleware(request, call_next):
    from app.core.database import db

    request.state.db = db
    response = await call_next(request)
    return response

from fastapi.responses import HTMLResponse

@app.get("/api/playground", response_class=HTMLResponse)
async def playground():
    return """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset=utf-8/>
        <title>GraphQL Playground</title>
        <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/graphql-playground-react/build/static/css/index.css" />
        <script src="//cdn.jsdelivr.net/npm/graphql-playground-react/build/static/js/middleware.js"></script>
      </head>
      <body>
        <div id="root" />
        <script>
          window.addEventListener('load', function (event) {
            GraphQLPlayground.init(document.getElementById('root'), {
              endpoint: '/api/graphql',
              headers: {
                "Content-Type": "application/json"
              },
              tabs: [
                {
                  endpoint: "http://localhost:8000/api/graphql"
                }
              ]
            })
          })
        </script>
      </body>
    </html>
    """



app.include_router(graphql_router, prefix="/api/graphql")
