from typing import Optional, List
import strawberry

@strawberry.type
class Component:
    name: str
    quantity: int

@strawberry.type
class Setup:
    player_count: int
    components: List[Component]

@strawberry.type
class Variant:
    title: str
    description: str

@strawberry.type
class Game:
    id: str
    title: str
    min_players: int
    max_players: int
    playtime: int
    setup: list[Setup]
    rules_summary: str
    variants: Optional[List[Variant]] = None
