from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
from players import Player
from tribe import Tribe
import json

load_dotenv()


def create_profile_image(player: Player, tribe: Tribe) -> str:
    client = OpenAI()

    response = client.images.generate(
        model="dall-e-3",
        prompt=f"A closeup portrait of a {player.generate_descriptors()} person standing on the beach in fiji. wearing casual {tribe.colors} tinted clothes.",
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url

    # Create the "images" folder if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Download the image file
    response = requests.get(image_url)
    if response.status_code == 200:
        # Extract the filename from the URL
        filename = player.get_full_name().replace(" ", "_")

        # Save the image file to the "images" folder
        with open(f"images/{filename}", "wb") as file:
            file.write(response.content)
            print(f"Image downloaded and saved as {filename}")
    else:
        print("Failed to download the image")


if __name__ == "__main__":
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful writing assistant, generating dialog for a reality TV show script. You will simulate dialog between characters.",
            },
            {
                "role": "system",
                "content": "Some info on the state of the game: The team stage is over, and we are now in the individual game. There are 9 players left in the game. The player felt confident they were safe before this challenge and wouldn't be voted out.",
            },
            {
                "role": "user",
                "content": 'The host, Jeff, says "Nice job on winning the challenge, you are safe from tribal council tonight. How does it feel?" Tim Kennedy replies:',
            },
        ],
        # tools=[
        #     {
        #         "type": "function",
        #         "function": {
        #             "name": "get_challenge_win_response",
        #             "description": "generates a line of dialog for a player that won a challenge.",
        #         },
        #     },
        # ],
    )

    print(completion.choices[0].message.content)
