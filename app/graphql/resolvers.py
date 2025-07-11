from app.graphql.types import Game, GameInput
import strawberry
from strawberry.types import Info
from bson import ObjectId, errors as bson_errors
from typing import Optional


def setup_input_to_dict(setup):
    return {
        "player_count": setup.player_count,
        "components": [component_input_to_dict(c) for c in setup.components]
}

def variant_input_to_dict(variant):
    return {
        "title": variant.title,
        "description": variant.description
}

def component_input_to_dict(component):
    return {
        "name": component.name,
        "quantity": component.quantity
}



async def add_game(game: GameInput, info: Info) -> Game:
    request = info.context["request"]
    db = request.state.db

    # Convert setup objects to dicts
    setup_list = [setup_input_to_dict(s) for s in game.setup]

    # Convert variants if any
    variants_list = None
    if game.variants is not None:
        variants_list = [variant_input_to_dict(v) for v in game.variants]

    game_dict = {
        "title": game.title,
        "min_players": game.min_players,
        "max_players": game.max_players,
        "playtime": game.playtime,
        "setup": setup_list,
        "rules_summary": game.rules_summary,
        "variants": variants_list
    }

    res = await db.games.insert_one(game_dict)
    game_dict["_id"] = res.inserted_id
    game_dict["id"] = str(game_dict.pop("_id"))

    return Game(**game_dict)


async def delete_game(id: str, info: Info) -> Optional[Game]:
    request = info.context["request"]
    db = request.state.db

    try:
        obj_id = ObjectId(id)
    except bson_errors.InvalidId:
        return None

    deleted_game = await db.games.find_one_and_delete({"_id": obj_id})

    if deleted_game:
        deleted_game["id"] = str(deleted_game.pop("_id"))
        return Game(**deleted_game)
    
    return None

async def update_game(id: str, game: GameInput, info: Info) -> Optional[Game]:
    request = info.context["request"]
    db = request.state.db

    try:
        obj_id = ObjectId(id)
    except bson_errors.InvalidId:
        return None
    
    filter_query = {"_id": obj_id}

    update_fields = {
        "title": game.title,
        "min_players": game.min_players,
        "max_players": game.max_players,
        "playtime": game.playtime,
        "rules_summary": game.rules_summary,
        "setup": game.setup
    }

    if game.variants is not None:
        update_fields["variants"] = game.variants

    updated_game = await db.games.find_one_and_update(
        filter_query,
        {"$set": update_fields},
        return_document=True
    )

    if updated_game:
        updated_game["id"] = str(updated_game.pop("_id"))
        return Game(**updated_game)

    return None

### Queries ###
async def get_boardgame_by_id(id: str, info: Info) -> Optional[Game]:
    request = info.context["request"]
    db = request.state.db
    
    try:
        obj_id = ObjectId(id)
    except bson_errors.InvalidId:
        return None
    
    game_dict = await db.games.find_one({"_id": obj_id})

    if game_dict:
        game_dict["id"] = str(game_dict.pop("_id"))
        return Game(**game_dict)

    return None

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
            playtime=doc["playtime"],
            rules_summary=doc["rules_summary"],
            setup=doc["setup"],
            variants=doc.get("variants"),
        )
        for doc in docs
    ]

    return games


@strawberry.type
class Mutation:
    addGame = strawberry.field(resolver=add_game)
    deleteGame = strawberry.field(resolver=delete_game)
    updateGame = strawberry.field(resolver=update_game)

@strawberry.type
class Query:
    games = strawberry.field(resolver=get_boardgames)
    findById = strawberry.field(resolver=get_boardgame_by_id)
