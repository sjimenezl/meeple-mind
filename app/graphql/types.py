from typing import Optional, List
import strawberry

@strawberry.type
class TurnStructure:
    steps: List[str]

@strawberry.type
class Component:
    name: str
    quantity: int

@strawberry.type
class Setup:
    player_count: int
    components: List[Component]

@strawberry.type
class SetupInstructions:
    description: str
    setup_number: int

@strawberry.type
class Variant:
    title: str
    description: str

@strawberry.type
class PlayerCountRules:
    player_count: int
    notes: str

@strawberry.type
class GeneralRule:
    description: str

@strawberry.type
class ScoringRule:
    description: str
    points: Optional[int] = None
    dynamic: Optional[str] = None  # e.g. "X points per 3 rows of 4"

@strawberry.type
class Game:
    id: str
    title: str
    goal: str
    general_rules: Optional[List[GeneralRule]] = None
    min_players: int
    max_players: int
    playtime: int
    setup: list[Setup]
    setup_instructions: Optional[List[SetupInstructions]] = None
    rules_summary: str
    start_player_condition: str
    turn_structure: list[TurnStructure]
    player_count_rules: Optional[List[PlayerCountRules]] = None
    scoring_rules: Optional[List[ScoringRule]] = None
    win_condition: str
    draw_condition: str
    end_condition: str
    variants: Optional[List[Variant]] = None

# Game inputs, mostly for insertions
@strawberry.input
class TurnStructureInput:
    steps: List[str]

@strawberry.input
class ComponentInput:
    name: str
    quantity: int

@strawberry.input
class SetupInput:
    player_count: int
    components: List[ComponentInput]

@strawberry.input
class SetupInstructionsInput:
    description: str
    setup_number: int

@strawberry.input
class VariantInput:
    title: str
    description: str

@strawberry.input
class PlayerCountRulesInput:
    player_count: int
    notes: str

@strawberry.input
class GeneralRuleInput:
    description: str

@strawberry.input
class ScoringRuleInput:
    description: str
    points: Optional[int] = None
    dynamic: Optional[str] = None

@strawberry.input
class GameInput:
    title: str
    goal: str
    general_rules: Optional[List[GeneralRuleInput]] = None
    min_players: int
    max_players: int
    playtime: int
    setup: list[SetupInput]
    setup_instructions: Optional[List[SetupInstructionsInput]] = None
    rules_summary: str
    start_player_condition: str
    turn_structure: list[TurnStructureInput]
    player_count_rules: Optional[List[PlayerCountRulesInput]] = None
    scoring_rules: Optional[List[ScoringRuleInput]] = None
    win_condition: str
    draw_condition: str
    end_condition: str
    variants: Optional[List[VariantInput]] = None