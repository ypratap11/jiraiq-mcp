#!/usr/bin/env python3
"""Test Jira connection and credentials"""

from jira import JIRA
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

def test_connection():
    """Test connection to Jira"""
    
    print("="*60)
    print("JIRA CONNECTION TEST")
    print("="*60)
    
    # Check env vars
    jira_url = os.getenv('JIRA_URL')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_token = os.getenv('JIRA_TOKEN')
    
    print("\nConfiguration:")
    print(f"  JIRA_URL: {jira_url}")
    print(f"  JIRA_EMAIL: {jira_email}")
    print(f"  JIRA_TOKEN: {'✓ Set' if jira_token else '✗ NOT SET'}")
    
    if not all([jira_url, jira_email, jira_token]):
        print("\n❌ ERROR: Missing credentials in .env file")
        print("\nSteps to fix:")
        print("  1. Copy .env.example to .env")
        print("  2. Edit .env with your actual credentials")
        print("  3. Get Jira token from: https://id.atlassian.com/manage-profile/security/api-tokens")
        return False
    
    print("\n" + "-"*60)
    print("Testing connection...")
    print("-"*60)
    
    try:
        # Connect
        jira = JIRA(
            server=jira_url,
            basic_auth=(jira_email, jira_token)
        )
        
        print("\n✅ Connected to Jira!")
        
        # Get user info
        user = jira.current_user()
        print(f"   Logged in as: {user}")
        
        # Try to get projects
        projects = jira.projects()
        print(f"   Accessible projects: {len(projects)}")
        
        if projects:
            print(f"\n   First few projects:")
            for p in projects[:5]:
                print(f"     - {p.key}: {p.name}")
        
        print("\n" + "="*60)
        print("✅ Everything looks good!")
        print("="*60)
        print("\nNext steps:")
        print("  1. Find an issue key from one of your projects")
        print("  2. Run: python scripts/analyze.py [ISSUE-KEY]")
        print("\nExample:")
        print("  python scripts/analyze.py ENG-1")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed!")
        print(f"   Error: {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Check your JIRA_URL includes https://")
        print("  2. Verify JIRA_EMAIL is your Atlassian account email")
        print("  3. Regenerate JIRA_TOKEN if needed:")
        print("     https://id.atlassian.com/manage-profile/security/api-tokens")
        return False

if __name__ == "__main__":
    test_connection()
