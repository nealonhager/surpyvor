from typing import List
from openai import OpenAI


def simulate_conversation(topic: str, players: List["Player"]):
    """
    Simulates a conversation between players about the topic.

    The first player in the players list starts the conversation.
    """
    player_names = [player.get_full_name() for player in players]
    client = OpenAI()
    prompt = f"{player_names[0]} says: I wanted to talk to you{'' if len(players) < 3 else ' all'} about {topic}."

    while True:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful writing assistant, generating dialog for a reality TV show script. You will simulate dialog between character(s): {player_names}",
                },
                {
                    "role": "system",
                    "content": "Keep in mind that any gameplay information that is shared can be abused by the others. Also note that someone will be eliminated.",
                },
                {
                    "role": "system",
                    "content": prompt,
                },
            ],
        )

        return completion.choices[0].message.content
