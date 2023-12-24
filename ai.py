from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="A closeup portrait of a pretty, healthy weight, not strong or weak body, medium curly black haired person standing on the beach in fiji. wearing casual green tinted clothes.",
    size="1024x1024",
    quality="standard",
    n=1,
)

image_url = response.data[0].url
print(image_url)
