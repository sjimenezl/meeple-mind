from app.graphql.types import Component, GeneralRule, PlayerCountRules, ScoringRule, Setup, SetupInstructions, TurnStructure, Variant


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