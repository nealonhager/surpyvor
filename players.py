from dataclasses import dataclass, field
from random import random, choices, choice
import names
from typing import List
import math


def get_random_job() -> str:
    """
    Opens the jobs.txt file and grabs a random job from the list.
    """
    with open("jobs.txt") as file:
        jobs = file.readlines()

    # Assign weights to each line based on their position in the file
    weights = [1 / (i + 1) for i in range(len(jobs))]

    # Choose a random line using the assigned weights
    random_line = choices(jobs, weights=weights, k=1)[0]

    return random_line.split(",")[0].replace(", All Other", "").strip().rstrip("s")


def generate_age() -> int:
    """
    Returns an age between 18 and 65, with it more likely to return a younger number.
    """
    ages = range(18, 60)
    weights = [1 / x for x in ages]
    return choices(ages, weights=weights, k=1)[0]


@dataclass
class Player:
    tribe: str = None
    first_name: str = field(default_factory=names.get_first_name)
    last_name: str = field(default_factory=names.get_last_name)
    age: int = field(default_factory=generate_age)
    profession: str = field(default_factory=get_random_job)
    advantages: list = field(default_factory=list)
    relationships: list = field(default_factory=list)
    votes: list = field(default_factory=list)
    times_voted_on: int = 0
    immunity_challenges_won: int = 0
    reward_challenges_won: int = 0
    votes_to_cast: int = 1
    hunger: float = 0

    # Attributes
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
    balance: float = field(default_factory=random)
    speed: float = field(default_factory=random)

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def vote(self, players: List["Player"]) -> "Player":
        random_player = choice(players)
        self.votes.append(random_player)
        return random_player

    def get_attributes(self) -> dict:
        """
        Returns a dict of the players attributes.
        """
        return {
            "agreeability": self.agreeability,
            "boldness": self.boldness,
            "strength": self.strength,
            "intelligence": self.intelligence,
            "emotional_intelligence": self.emotional_intelligence,
            "endurance": self.endurance,
            "charisma": self.charisma,
            "loyalty": self.loyalty,
            "strategic_ability": self.strategic_ability,
            "popularity": self.popularity,
            "survival_skills": self.survival_skills,
            "creativity": self.creativity,
            "fortitude": self.fortitude,
            "pride": self.pride,
            "balance": self.balance,
            "speed": self.speed,
        }

    def calculate_attributes_product(self) -> float:
        """
        Returns the product of all the player's attributes.
        """

        return math.prod(list(self.get_attributes().values()))

    @staticmethod
    def get_attribute_names() -> List[str]:
        return [
            "agreeability",
            "boldness",
            "strength",
            "intelligence",
            "emotional_intelligence",
            "endurance",
            "charisma",
            "loyalty",
            "strategic_ability",
            "popularity",
            "survival_skills",
            "creativity",
            "fortitude",
            "pride",
            "balance",
            "speed",
        ]


host = Player(tribe="None", first_name="Jeff", last_name="Probst", age=50)
