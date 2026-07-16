import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Hello Claude! Reply in one sentence."}
    ]
)

print(message.content[0].text)