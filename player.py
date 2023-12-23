from dataclasses import dataclass, field
from random import random, randint
import names


def get_random_job() -> str:
    """Opens the jobs.txt file and grabs a random job from the list."""
    with open("jobs.txt") as file:
        jobs = file.readlines()
    return jobs[randint(0, len(jobs) - 1)].strip()


def generate_age() -> int:
    """Returns an age between 18 and 65"""
    return randint(18, 65)

@dataclass
class Player:
    tribe: str = None
    first_name: str = field(default_factory=names.get_first_name)
    last_name: str = field(default_factory=names.get_last_name)
    age: int = field(default_factory=generate_age)
    profession: str = field(default_factory=get_random_job)
    advantages: list = field(default_factory=list)
    relationships: list = field(default_factory=list)
    times_voted_on: int = 0
    immunity_challenges_won: int = 0
    reward_challenges_won: int = 0
    votes_to_cast: int = 1
    hunger: float = 0

    agreeability: float = field(default_factory=random)
    boldness: float = field(default_factory=random)
    strength: float = field(default_factory=random)
    intelligence: float = field(default_factory=random)
    emotional_intelligence: float = field(default_factory=random)
    endurance: float = field(default_factory=random)
    charisma: float = field(default_factory=random)
    loyalty: float = field(default_factory=random)
    strategic_ability: float = field(default_factory=random)
    popularity: float = field(default_factory=random)
    survival_skills: float = field(default_factory=random)
    creativity: float = field(default_factory=random)
    fortitude: float = field(default_factory=random)
    pride: float = field(default_factory=random)
