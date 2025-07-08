from app.graphql.types import Game
import strawberry
from strawberry.types import Info

def add_game(title: str, playtime: int) -> Game:
    print(f"Adding {title}, playtime {playtime}")
    return Game(title=title, playtime=playtime)

async def get_boardgames(info: Info) -> list[Game]:
    request = info.context["request"]
    db = request.state.db
    docs = await db.games.find().to_list(length=None)
    games = [
        Game(
            id=str(doc["_id"]),
            title=doc["title"],
            min_players=doc["min_players"],
            max_players=doc["max_players"],
            playtime=doc.get("playtime"),
            rules_summary=doc.get("rules_summary"),
            setup=doc.get("setup"),
            variants=doc.get("variants"),
        )
        for doc in docs
    ]

    return games


@strawberry.type
class Mutation:
    addGame = strawberry.field(resolver=add_game)

@strawberry.type
class Query:
    games = strawberry.field(resolver=get_boardgames)
