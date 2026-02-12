import asyncio
from jiraiq_server import analyze_issue

async def main():
    print("="*80)
    print("Testing JiraIQ MCP Server")
    print("="*80)
    print()
    
    # Get issue key from user
    issue_key = input("Enter a Jira issue key to analyze (e.g., ENG-1): ").strip().upper()
    
    if not issue_key:
        print("❌ No issue key provided. Using ENG-1 as default.")
        issue_key = "ENG-1"
    
    print(f"\n🔍 Analyzing {issue_key}...\n")
    
    try:
        # Test executive template
        result = await analyze_issue({
            "issue_key": issue_key,
            "template": "executive"
        })
        
        print("="*80)
        print("EXECUTIVE TEMPLATE RESULT:")
        print("="*80)
        print(result[0].text)
        print()
        
        print("="*80)
        print("✅ MCP Server Test PASSED!")
        print("="*80)
        print()
        print("Your MCP server is working correctly!")
        print("Next step: Connect it to Claude Desktop")
        
    except Exception as e:
        print("="*80)
        print("❌ MCP Server Test FAILED!")
        print("="*80)
        print(f"Error: {str(e)}")
        print()
        print("Troubleshooting:")
        print("1. Make sure .env file has correct credentials")
        print("2. Verify the issue key exists and you have access")
        print("3. Check that jiraiq_server.py is in the same directory")

if __name__ == "__main__":
    asyncio.run(main())
