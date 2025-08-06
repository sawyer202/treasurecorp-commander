from anthropic import Anthropic
import os

# Set your API key from environment variable
api_key = os.getenv("ANTHROPIC_API_KEY")

# Initialize Anthropic client
client = Anthropic(api_key=api_key)

# Get content
try:
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=300,
        messages=[
            {"role": "user", "content": "Create a single Twitter post about DAO treasury analytics"}
        ]
    )
    print(message.content[0].text)
except Exception as e:
    print(f"Error: {e}")

# Keep window open
input("Press Enter to exit...")
# Keep the window open until user presses Enter
print("\nPress Enter to exit...")
input()