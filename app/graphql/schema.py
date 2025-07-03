from app.graphql.resolvers import Mutation, Query
import strawberry

schema = strawberry.Schema(
    query=Query, 
    mutation = Mutation
)
