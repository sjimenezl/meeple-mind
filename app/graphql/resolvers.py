from app.graphql.types import Game
import strawberry
import typing
from strawberry.types import Info

def add_game(title: str, playtime: int) -> Game:
    print(f"Adding {title}, playtime {playtime}")
    return Game(title=title, playtime=playtime)

def get_playtime() -> typing.List[Game]:
    return [Game(playtime=20)]

async def get_boardgames(info: Info) -> typing.List[Game]:
    db = info.context.request.state.db
    docs = await db.games.find().to_list(length=None)
    return [Game(**doc) for doc in docs]

@strawberry.type
class Mutation:
    addGame = strawberry.field(resolver=add_game)

@strawberry.type
class Query:
    games = strawberry.field(resolver=get_boardgames)
    playtimes = strawberry.field(resolver=get_playtime)
