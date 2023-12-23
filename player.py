from dataclasses import dataclass
from random import random


@dataclass
class Player:
    name: str
    age: int
    profession: str
    advantages: list = []
    relationships: list = []
    times_voted_on: int = 0
    immunity_challenges_won: int = 0
    reward_challenges_won: int = 0
    tribe: str
    votes_to_cast: int = 1
    hunger: float = 0

    agreeability: float = random()
    boldness: float = random()
    strength: float = random()
    intelligence: float = random()
    emotional_intelligence: float = random()
    endurance: float = random()
    charisma: float = random()
    loyalty: float = random()
    strategic_ability: float = random()
    popularity: float = random()
    survival_skills: float = random()
    creativity: float = random()
    fortitude: float = random()
