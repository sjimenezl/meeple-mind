from app.graphql.types import Component, Game, GameInput, GeneralRule, PlayerCountRules, ScoringRule, Setup, SetupInstructions, TurnStructure, Variant
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

def setup_instructions_input_to_dict(instructions):
    return {
        "description": instructions.description,
        "setup_number": instructions.setup_number
    }

def turn_structure_input_to_dict(structure):
    return {
        "steps": structure.steps
    }

def player_count_rules_input_to_dict(player_rules):
    return {
        "player_count": player_rules.player_count,
        "notes": player_rules.notes
    }

def general_rule_input_to_dict(rule):
    return {"description": rule.description}

def dict_to_component(d: dict) -> Component:
    return Component(
        name=d["name"],
        quantity=d["quantity"]
    )

def dict_to_setup(d: dict) -> Setup:
    return Setup(
        player_count=d["player_count"],
        components=[dict_to_component(c) for c in d["components"]]
    )

def dict_to_turn_structure(d: dict) -> TurnStructure:
    return TurnStructure(
        steps=d["steps"]
    )

def dict_to_setup_instruction(d: dict) -> SetupInstructions:
    return SetupInstructions(
        description=d["description"],
        setup_number=d["setup_number"]
    )

def dict_to_player_count_rule(d: dict) -> PlayerCountRules:
    return PlayerCountRules(
        player_count=d["player_count"],
        notes=d["notes"]
    )

def dict_to_variant(d: dict) -> Variant:
    return Variant(
        title=d["title"],
        description=d["description"]
    )

def dict_to_general_rule(d: dict) -> GeneralRule:
    return GeneralRule(
        description=d["description"]
    )

def dict_to_scoring_rule(d: dict) -> ScoringRule:
    return ScoringRule(
        description=d["description"],
        points=d.get("points"),
        dynamic=d.get("dynamic")
    )

async def add_game(game: GameInput, info: Info) -> Game:
    request = info.context["request"]
    db = request.state.db

    # Convert setup objects to dicts
    setup_list = [setup_input_to_dict(s) for s in game.setup]

    # Convert variants if any
    variants_list = None
    if game.variants is not None:
        variants_list = [variant_input_to_dict(v) for v in game.variants]

    # Convert setup instructions if any
    setup_instructions_list = None
    if game.setup_instructions is not None:
        setup_instructions_list = [setup_instructions_input_to_dict(si) for si in game.setup_instructions]

    turn_structure_list = [turn_structure_input_to_dict(t) for t in game.turn_structure]

    player_count_rules_list = None
    if game.player_count_rules is not None:
        player_count_rules_list = [player_count_rules_input_to_dict(pc) for pc in game.player_count_rules]
    
    game_dict = {
        "title": game.title,
        "goal": game.goal,
        "general_rules": game.general_rules,
        "min_players": game.min_players,
        "max_players": game.max_players,
        "playtime": game.playtime,
        "setup": setup_list,
        "setup_instructions": setup_instructions_list,
        "rules_summary": game.rules_summary,
        "start_player_condition": game.start_player_condition,
        "turn_structure": turn_structure_list,
        "player_count_rules": player_count_rules_list,
        "win_condition": game.win_condition,
        "draw_condition": game.draw_condition,
        "end_condition": game.end_condition,
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
        "goal": game.goal,
        "min_players": game.min_players,
        "max_players": game.max_players,
        "playtime": game.playtime,
        "rules_summary": game.rules_summary,
        "setup": [setup_input_to_dict(s) for s in game.setup],
        "start_player_condition": game.start_player_condition,
        "win_condition": game.win_condition,
        "draw_condition": game.draw_condition,
        "end_condition": game.end_condition
    }

    if game.general_rules is not None:
        update_fields["general_rules"] = [general_rule_input_to_dict(gr) for gr in game.general_rules]

    if game.variants is not None:
        update_fields["variants"] = [variant_input_to_dict(v) for v in game.variants]
    
    if game.setup_instructions is not None:
        update_fields["setup_instructions"] = [setup_instructions_input_to_dict(si) for si in game.setup_instructions]

    if game.turn_structure is not None:
        update_fields["turn_structure"] = [turn_structure_input_to_dict(ts) for ts in game.turn_structure]

    if game.player_count_rules is not None:
        update_fields["player_count_rules"] = [player_count_rules_input_to_dict(pcr) for pcr in game.player_count_rules]

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
            goal=doc["goal"],
            general_rules=[dict_to_general_rule(r) for r in doc.get("general_rules", [])] if doc.get("general_rules") else None,
            min_players=doc["min_players"],
            max_players=doc["max_players"],
            playtime=doc["playtime"],
            setup=[dict_to_setup(s) for s in doc["setup"]],
            setup_instructions=[dict_to_setup_instruction(i) for i in doc.get("setup_instructions", [])] if doc.get("setup_instructions") else None,
            rules_summary=doc["rules_summary"],
            start_player_condition=doc["start_player_condition"],
            turn_structure=[dict_to_turn_structure(t) for t in doc["turn_structure"]],
            player_count_rules=[dict_to_player_count_rule(p) for p in doc.get("player_count_rules", [])] if doc.get("player_count_rules") else None,
            scoring_rules=[dict_to_scoring_rule(r) for r in doc.get("scoring_rules", [])] if doc.get("scoring_rules") else None,
            win_condition=doc["win_condition"],
            draw_condition=doc["draw_condition"],
            end_condition=doc["end_condition"],
            variants=[dict_to_variant(v) for v in doc.get("variants", [])] if doc.get("variants") else None,
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
