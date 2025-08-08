from app.graphql.types import Game, GameInput
import strawberry
from strawberry.types import Info
from bson import ObjectId, errors as bson_errors
from typing import Optional

from app.helper.helpers import *
from app.models.models import GameModel

async def add_game(game: GameInput, info: Info) -> GameModel:
    request = info.context["request"]
    db = request.state.db

    game_dict = game.to_pydantic().model_dump()

    res = await db.games.insert_one(game_dict)
    game_dict["_id"] = res.inserted_id
    game_dict["id"] = str(game_dict.pop("_id"))

    return GameModel.model_validate(game_dict)


async def delete_game(id: str, info: Info) -> Optional[GameModel]:
    request = info.context["request"]
    db = request.state.db

    try:
        obj_id = ObjectId(id)
    except bson_errors.InvalidId:
        return None

    deleted_game = await db.games.find_one_and_delete({"_id": obj_id})

    if deleted_game:
        deleted_game["id"] = str(deleted_game.pop("_id"))
        return GameModel.model_validate(deleted_game)
    
    return None

async def update_game(id: str, game: GameInput, info: Info) -> Optional[GameModel]:
    request = info.context["request"]
    db = request.state.db

    try:
        obj_id = ObjectId(id)
    except bson_errors.InvalidId:
        return None

    filter_query = {"_id": obj_id}

    # Turns GameInput (Strawberry dataclass) to GameModel (Pydantic)
    update_fields = game.to_pydantic().model_dump(exclude_unset=True)

    updated_game = await db.games.find_one_and_update(
        filter_query,
        {"$set": update_fields},
        return_document=True
    )

    if updated_game:
        updated_game["id"] = str(updated_game.pop("_id"))
        return GameModel.model_validate(updated_game)

    return None

### Queries ###

# TODO: FIND A CLEANER VERSION OF THIS MESS
async def get_boardgame_by_id(id: str, info: Info) -> Optional[GameModel]:
    request = info.context["request"]
    db = request.state.db

    try:
        obj_id = ObjectId(id)
    except bson_errors.InvalidId:
        return None

    game_dict = await db.games.find_one({"_id": obj_id})
    if not game_dict:
        return None

    game_dict["id"] = str(game_dict.pop("_id"))
    return GameModel.model_validate(game_dict)

async def get_boardgames(info: Info) -> list[GameModel]:
    request = info.context["request"]
    db = request.state.db

    docs = await db.games.find().to_list(length=None)

    for doc in docs:
        doc["id"] = str(doc.pop("_id"))

    return [GameModel.model_validate(doc) for doc in docs]


@strawberry.type
class Mutation:
    @strawberry.field
    async def add_game(self, game: GameInput, info: Info) -> Optional[Game]:
        return await add_game(game, info)
    
    @strawberry.field
    async def update_game(self, id: str, game: GameInput, info: Info) -> Optional[Game]:
        return await update_game(id, game, info)
    
    @strawberry.field
    async def delete_game(self, id: str, info: Info) -> Optional[Game]:
        return await delete_game(id, info)
    # addGame = strawberry.field(resolver=add_game)
    # deleteGame = strawberry.field(resolver=delete_game)
    # updateGame = strawberry.field(resolver=update_game)

@strawberry.type
class Query:
    @strawberry.field
    async def find_by_id(self, id: str, info: Info) -> Optional[Game]:
        return await get_boardgame_by_id(id, info)

    @strawberry.field
    async def games(self, info: Info) -> list[Game]:
        return await get_boardgames(info)
