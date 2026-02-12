from jira import JIRA
from dotenv import load_dotenv
import os

load_dotenv()

print("Testing Jira connection...")

jira = JIRA(
    server=os.getenv('JIRA_URL'),
    basic_auth=(os.getenv('JIRA_EMAIL'), os.getenv('JIRA_TOKEN'))
)

projects = jira.projects()
print(f"\n✅ Connected to Jira!")
print(f"Found {len(projects)} projects:")
for p in projects[:5]:
    print(f"  - {p.key}: {p.name}")

print("\n" + "="*60)
print("Jira connection test PASSED!")
print("="*60)
