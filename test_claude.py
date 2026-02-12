from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

print("Testing Claude AI connection...")

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=50,
    messages=[{"role": "user", "content": "Say: JiraIQ MCP server is ready to go!"}]
)

print("\n✅ Claude AI connected!")
print(f"Response: {response.content[0].text}")

print("\n" + "="*60)
print("Claude AI connection test PASSED!")
print("="*60)
