import os

from google import genai
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Read API key from .env
API_KEY = os.getenv("GEMINI_API_KEY")
print("Loaded Key:", API_KEY[:15])

print("API Key Loaded:", API_KEY is not None)

# Create Gemini client
client = genai.Client(
    api_key=API_KEY
)


def extract_road_name(user_input):

    prompt = f"""
Extract only the road name from this complaint.

Complaint:
{user_input}

Return only the road name.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()


if __name__ == "__main__":

    test_input = "There is a pothole near Anna Salai"

    road = extract_road_name(test_input)

    print("Extracted Road:", road)