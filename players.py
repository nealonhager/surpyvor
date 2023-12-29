from dataclasses import dataclass, field
from random import random, choices, choice
import names
from typing import List
import math
import os
import requests
from openai import OpenAI


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


def generate_race() -> str:
    return choice(
        [
            "white",
            "asian",
            "black",
            "hispanic",
            "arabic",
        ]
    )


def generate_age() -> int:
    """
    Returns an age between 18 and 65, with it more likely to return a younger number.
    """
    ages = range(18, 60)
    weights = [1 / x for x in ages]
    return choices(ages, weights=weights, k=1)[0]


def generate_home_state() -> str:
    """
    Randomly selects a state from the USA.
    """
    return choice(
        [
            "Alabama",
            "Alaska",
            "Arizona",
            "Arkansas",
            "California",
            "Colorado",
            "Connecticut",
            "Delaware",
            "Florida",
            "Georgia",
            "Hawaii",
            "Idaho",
            "Illinois",
            "Indiana",
            "Iowa",
            "Kansas",
            "Kentucky",
            "Louisiana",
            "Maine",
            "Maryland",
            "Massachusetts",
            "Michigan",
            "Minnesota",
            "Mississippi",
            "Missouri",
            "Montana",
            "Nebraska",
            "Nevada",
            "New Hampshire",
            "New Jersey",
            "New Mexico",
            "New York",
            "North Carolina",
            "North Dakota",
            "Ohio",
            "Oklahoma",
            "Oregon",
            "Pennsylvania",
            "Rhode Island",
            "South Carolina",
            "South Dakota",
            "Tennessee",
            "Texas",
            "Utah",
            "Vermont",
            "Virginia",
            "Washington",
            "West Virginia",
            "Wisconsin",
            "Wyoming",
        ]
    )


@dataclass
class Player:
    tribe = None
    gender = None
    first_name = None
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
    home_state: str = field(default_factory=generate_home_state)

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

    # Descriptor
    descriptor: str = ""

    def __post_init__(self):
        self.gender = choice(["male", "female"])
        self.first_name = names.get_first_name(gender=self.gender)

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def vote(self, players: List["Player"]) -> "Player":
        players = players.copy()
        try:
            players.remove(self)
        except:
            pass
        random_player = choice(players)
        print(
            f"{self.get_full_name()} cast their vote on {random_player.get_full_name()}".upper()
        )
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

    def generate_descriptors(self) -> str:
        if self.descriptor == "":
            weight = random()

            weight = (
                "overweight"
                if weight > 0.66
                else "underweight"
                if weight < 0.33
                else "healthy weight"
            )
            strength = (
                "strong body"
                if self.strength > 0.66
                else "weak body"
                if self.strength < 0.33
                else "not strong or weak body"
            )

            hair_color = choice(["black", "brown", "blonde", "red"])
            hair_type = choice(["straight", "curly", "wavy"])
            hair_length = choice(["long", "short", "medium"])
            hair_thickness = choice(["thick", "thin"])
            balding = bool(range(0, 2))
            hair_description = f"{'balding ' if balding and self.gender == 'male' else ''}{hair_length} {hair_thickness} {hair_type} {hair_color}"

            self.descriptor = f"{weight}, {strength}, {hair_description} haired"

        return self.descriptor

    def calculate_attributes_product(self) -> float:
        """
        Returns the product of all the player's attributes.
        """

        return math.prod(list(self.get_attributes().values()))

    def get_challenge_win_speech(self) -> str:
        client = OpenAI()

        player_info = self.get_attributes()
        player_info["hunger"] = self.hunger
        player_info["home_state"] = self.home_state

        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful writing assistant, generating dialog for a reality TV show script. You will simulate dialog between characters.",
                },
                {
                    "role": "system",
                    "content": f"Some info on the player (if the value is a decimal, the range is from 0-1): {str(player_info)}.",
                },
                {
                    "role": "user",
                    "content": "The host, Jeff, says: Nice job on winning the challenge, you are safe from tribal council tonight. How does it feel?",
                },
                {
                    "role": "user",
                    "content": "The player replies: ",
                },
            ],
        )

        response = completion.choices[0].message.content
        return response

    def create_profile_image(self, tribe_color: str) -> str:
        client = OpenAI()
        prompt = f"A closeup portrait of a {self.generate_descriptors()} {generate_race()} {self.gender}. {self.age} years old. Standing on an empty beach in fiji. sunny day. wearing casual {tribe_color} clothes."
        attempts = 3
        while True:
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                print(prompt)
                image_url = response.data[0].url

                # Create the "images" folder if it doesn't exist
                os.makedirs("images", exist_ok=True)

                # Download the image file
                response = requests.get(image_url)

                # Extract the filename from the URL
                filename = self.get_full_name().replace(" ", "_")

                # Save the image file to the "images" folder
                with open(f"images/{filename}.png", "wb") as file:
                    file.write(response.content)
                    print(f"Image downloaded and saved as {filename}")

                break
            except:
                if attempts == 0:
                    raise Exception(f"couldn't get an image for {self.get_full_name()}")

                attempts -= 1

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


host = Player()
host.first_name = "Jeff"
host.last_name = "Probst"
