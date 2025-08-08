from typing import List, Optional
from pydantic import BaseModel

class TurnStructureModel(BaseModel):
    steps: List[str]

class ComponentModel(BaseModel):
    name: str
    quantity: int

class SetupModel(BaseModel):
    player_count: int
    components: List[ComponentModel]

class SetupInstructionsModel(BaseModel):
    description: str
    setup_number: int

class VariantModel(BaseModel):
    title: str
    description: str

class PlayerCountRulesModel(BaseModel):
    player_count: int
    notes: str

class GeneralRuleModel(BaseModel):
    description: str

class ScoringRuleModel(BaseModel):
    description: str
    points: Optional[int] = None
    dynamic: Optional[str] = None  # e.g. "X points per 3 rows of 4"

class GameModel(BaseModel):
    id: str
    title: str
    goal: str
    general_rules: Optional[List[GeneralRuleModel]] = None
    min_players: int
    max_players: int
    playtime: int
    setup: list[SetupModel]
    setup_instructions: Optional[List[SetupInstructionsModel]] = None
    rules_summary: str
    start_player_condition: str
    turn_structure: list[TurnStructureModel]
    player_count_rules: Optional[List[PlayerCountRulesModel]] = None
    scoring_rules: Optional[List[ScoringRuleModel]] = None
    win_condition: str
    draw_condition: str
    end_condition: str
    variants: Optional[List[VariantModel]] = None

class GameModelInput(BaseModel):
    title: str
    goal: str
    general_rules: Optional[List[GeneralRuleModel]] = None
    min_players: int
    max_players: int
    playtime: int
    setup: list[SetupModel]
    setup_instructions: Optional[List[SetupInstructionsModel]] = None
    rules_summary: str
    start_player_condition: str
    turn_structure: list[TurnStructureModel]
    player_count_rules: Optional[List[PlayerCountRulesModel]] = None
    scoring_rules: Optional[List[ScoringRuleModel]] = None
    win_condition: str
    draw_condition: str
    end_condition: str
    variants: Optional[List[VariantModel]] = None