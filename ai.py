from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="A closeup portrait of an ugly person wearing mostly the color orange casual clothing, on a beach of fiji. mid day.",
    size="1024x1024",
    quality="standard",
    n=1,
)

image_url = response.data[0].url
print(image_url)
