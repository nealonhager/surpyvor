from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
from players import Player
from tribe import Tribe

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
