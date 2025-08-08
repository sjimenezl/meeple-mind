from typing import Optional, List
import strawberry

from strawberry.experimental.pydantic import type as pydantic_type
from strawberry.experimental.pydantic import input as pydantic_input

from app.models.models import *

@pydantic_type(model=ComponentModel, all_fields=True)
class Component:
    pass

@pydantic_type(model=SetupModel, all_fields=True)
class Setup:
    pass

@pydantic_type(model=SetupInstructionsModel, all_fields=True)
class SetupInstructions:
    pass

@pydantic_type(model=VariantModel, all_fields=True)
class Variant:
    pass

@pydantic_type(model=PlayerCountRulesModel, all_fields=True)
class PlayerCountRules:
    pass

@pydantic_type(model=GeneralRuleModel, all_fields=True)
class GeneralRule:
    pass

@pydantic_type(model=ScoringRuleModel, all_fields=True)
class ScoringRule:
    pass

@pydantic_type(model=TurnStructureModel, all_fields=True)
class TurnStructure:
    pass

@pydantic_type(model=GameModel, all_fields=True)
class Game:
    pass

# Game inputs, mostly for insertions
@pydantic_input(model=TurnStructureModel, all_fields=True)
class TurnStructureInput:
    pass

@pydantic_input(model=ComponentModel, all_fields=True)
class ComponentInput: 
    pass

@pydantic_input(model=SetupModel, all_fields=True)
class SetupInput: 
    pass

@pydantic_input(model=SetupInstructionsModel, all_fields=True)
class SetupInstructionsInput:
    pass

@pydantic_input(model=VariantModel, all_fields=True)
class VariantInput:
    pass

@pydantic_input(model=PlayerCountRulesModel, all_fields=True)
class PlayerCountRulesInput:
    pass

@pydantic_input(model=GeneralRuleModel, all_fields=True)
class GeneralRuleInput:
    pass

@pydantic_input(model=ScoringRuleModel, all_fields=True)
class ScoringRuleInput:
    pass

@pydantic_input(model=GameModelInput, all_fields=True)
class GameInput:
    pass