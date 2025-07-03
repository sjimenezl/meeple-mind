
from app.graphql.types import Game
import strawberry
import typing

def add_game(self, title: str, playtime: int) -> Game: 
    print(f"Adding {title}, playtime {playtime}")

    return Game(title=title, playtime=playtime)

@strawberry.type
class Mutation:
    addGame: Game = strawberry.field(resolver=add_game)

def get_boardgames():
    return [
        Game(
            title="The Great Gatsby",
            playtime=23
        ),
    ]

def get_playtime():
    return [Game(playtime=20)]

@strawberry.type
class Query:
    games: typing.List[Game] = strawberry.field(resolver=get_boardgames)
    playtimes: typing.List[Game] = strawberry.field(resolver=get_playtime)