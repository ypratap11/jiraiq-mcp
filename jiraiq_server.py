#!/usr/bin/env python3
"""
JiraIQ MCP Server
Provides Jira analysis tools for Claude
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import os
from jira import JIRA
from anthropic import Anthropic
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize MCP server
app = Server("jiraiq")

# Initialize Jira client
def get_jira_client():
    """Initialize Jira client with credentials from environment"""
    return JIRA(
        server=os.getenv('JIRA_URL'),
        basic_auth=(os.getenv('JIRA_EMAIL'), os.getenv('JIRA_TOKEN'))
    )

# Initialize Anthropic client
def get_anthropic_client():
    """Initialize Anthropic client"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment")
    return Anthropic(api_key=api_key)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available JiraIQ tools"""
    return [
        Tool(
            name="analyze_jira_issue",
            description="Analyze a Jira issue and generate stakeholder-specific reports (executive, technical, or PM format)",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {
                        "type": "string",
                        "description": "Jira issue key (e.g., ENG-123, PROJ-456)"
                    },
                    "template": {
                        "type": "string",
                        "enum": ["executive", "technical", "pm", "all"],
                        "description": "Report template: executive (for leadership), technical (for engineers), pm (for product managers), or all (generates all three)",
                        "default": "executive"
                    }
                },
                "required": ["issue_key"]
            }
        ),
        Tool(
            name="find_blocked_issues",
            description="Find all blocked or at-risk issues in a Jira project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_key": {
                        "type": "string",
                        "description": "Jira project key (e.g., ENG, PROJ)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of issues to return (default: 10)",
                        "default": 10
                    }
                },
                "required": ["project_key"]
            }
        ),
        Tool(
            name="analyze_sprint",
            description="Analyze all issues in the current or specified sprint to identify blockers, risks, and team sentiment",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_key": {
                        "type": "string",
                        "description": "Jira project key (e.g., ENG, PROJ)"
                    },
                    "sprint_name": {
                        "type": "string",
                        "description": "Sprint name (optional, defaults to active sprint)"
                    }
                },
                "required": ["project_key"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle JiraIQ tool calls"""
    
    try:
        if name == "analyze_jira_issue":
            return await analyze_issue(arguments)
        elif name == "find_blocked_issues":
            return await find_blocked(arguments)
        elif name == "analyze_sprint":
            return await analyze_sprint_tool(arguments)
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}\n\nPlease check your Jira credentials and issue key."
        )]


async def analyze_issue(arguments: dict) -> list[TextContent]:
    """Analyze a single Jira issue"""
    
    issue_key = arguments["issue_key"].upper()
    template = arguments.get("template", "executive")
    
    # Get Jira client
    jira = get_jira_client()
    
    # Fetch issue
    try:
        issue = jira.issue(issue_key)
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Could not fetch issue {issue_key}. Error: {str(e)}\n\nPlease verify the issue key exists and you have access."
        )]
    
    # Get comments
    comments = issue.fields.comment.comments
    
    # Build analysis prompt
    comment_text = "\n\n".join([
        f"{c.author.displayName} ({c.created}): {c.body}"
        for c in comments
    ]) if comments else "No comments yet."
    
    priority = issue.fields.priority.name if hasattr(issue.fields, 'priority') and issue.fields.priority else 'Not set'
    
    prompt = f"""Analyze this Jira issue for blockers, risks, and team sentiment:

Issue: {issue.fields.summary}
Type: {issue.fields.issuetype.name}
Status: {issue.fields.status.name}
Priority: {priority}

Comments:
{comment_text}

Provide:
1. Team Sentiment: Assess if the team mood is positive, neutral, or negative based on comment tone
2. Active Blockers: Identify any blockers mentioned (YES/NO and what they are)
3. Biggest Risk: What could go wrong or delay this issue
4. Actionable Recommendation: One specific next step to unblock or move forward

Be concise and quote specific comments when relevant."""
    
    # Get AI analysis
    anthropic = get_anthropic_client()
    
    response = anthropic.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2000,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    
    analysis = response.content[0].text
    
    # Format based on template
    if template == "executive":
        output = format_executive(issue, analysis)
    elif template == "technical":
        output = format_technical(issue, comments, analysis)
    elif template == "pm":
        output = format_pm(issue, comments, analysis)
    else:  # all
        output = f"""EXECUTIVE SUMMARY:
{'='*80}
{format_executive(issue, analysis)}

{'='*80}

TECHNICAL ANALYSIS:
{'='*80}
{format_technical(issue, comments, analysis)}

{'='*80}

PM REPORT:
{'='*80}
{format_pm(issue, comments, analysis)}"""
    
    return [TextContent(type="text", text=output)]


async def find_blocked(arguments: dict) -> list[TextContent]:
    """Find blocked issues in a project"""
    
    project_key = arguments["project_key"].upper()
    limit = arguments.get("limit", 10)
    
    jira = get_jira_client()
    
    # Search for potentially blocked issues
    jql = f'project = {project_key} AND status != Done AND (labels = blocked OR description ~ "blocked" OR comment ~ "blocked" OR status = Blocked)'
    
    try:
        issues = jira.search_issues(jql, maxResults=limit)
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Could not search project {project_key}. Error: {str(e)}"
        )]
    
    if not issues:
        return [TextContent(
            type="text",
            text=f"✅ No blocked issues found in {project_key}. All clear!"
        )]
    
    # Format results
    output = f"🚨 Found {len(issues)} potentially blocked issue(s) in {project_key}:\n\n"
    
    for i, issue in enumerate(issues, 1):
        priority = issue.fields.priority.name if hasattr(issue.fields, 'priority') and issue.fields.priority else 'N/A'
        assignee = issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned'
        
        output += f"{i}. **{issue.key}**: {issue.fields.summary}\n"
        output += f"   Status: {issue.fields.status.name} | Priority: {priority} | Owner: {assignee}\n"
        
        # Check for blocker indicators in recent comments
        comments = issue.fields.comment.comments[-3:] if issue.fields.comment.comments else []
        blocker_mentions = []
        for c in comments:
            if 'block' in c.body.lower():
                blocker_mentions.append(f"   💬 {c.author.displayName}: \"{c.body[:80]}...\"")
        
        if blocker_mentions:
            output += "\n".join(blocker_mentions) + "\n"
        
        output += "\n"
    
    output += f"\n💡 Tip: Use 'analyze_jira_issue' with each issue key to get detailed analysis and recommendations."
    
    return [TextContent(type="text", text=output)]


async def analyze_sprint_tool(arguments: dict) -> list[TextContent]:
    """Analyze a sprint's health"""
    
    project_key = arguments["project_key"].upper()
    sprint_name = arguments.get("sprint_name")
    
    jira = get_jira_client()
    
    # Build JQL for sprint
    if sprint_name:
        jql = f'project = {project_key} AND sprint = "{sprint_name}" AND status != Done'
    else:
        jql = f'project = {project_key} AND sprint in openSprints() AND status != Done'
    
    try:
        issues = jira.search_issues(jql, maxResults=50)
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Could not analyze sprint for {project_key}. Error: {str(e)}"
        )]
    
    if not issues:
        return [TextContent(
            type="text",
            text=f"No open issues found in sprint for {project_key}"
        )]
    
    # Categorize issues
    blocked = []
    high_activity = []
    stale = []
    
    for issue in issues:
        comments = issue.fields.comment.comments
        
        # Check if blocked
        is_blocked = (
            hasattr(issue.fields, 'labels') and 'blocked' in [l.lower() for l in issue.fields.labels] or
            issue.fields.status.name.lower() == 'blocked' or
            any('block' in c.body.lower() for c in comments[-3:])
        )
        
        if is_blocked:
            blocked.append(issue)
        elif len(comments) > 5:
            high_activity.append(issue)
        elif len(comments) == 0:
            stale.append(issue)
    
    # Generate summary
    output = f"📊 SPRINT HEALTH REPORT: {project_key}\n"
    output += f"{'='*80}\n\n"
    output += f"Total Issues: {len(issues)}\n"
    output += f"Blocked: {len(blocked)} 🔴\n"
    output += f"High Activity: {len(high_activity)} 🟡\n"
    output += f"Stale (no comments): {len(stale)} 💤\n\n"
    
    if blocked:
        output += "🚨 BLOCKED ISSUES (Need Immediate Attention):\n"
        output += "-" * 80 + "\n"
        for issue in blocked[:5]:
            output += f"• {issue.key}: {issue.fields.summary}\n"
            output += f"  Status: {issue.fields.status.name}\n\n"
    
    if high_activity:
        output += "\n🔥 HIGH ACTIVITY ISSUES (Active Discussion):\n"
        output += "-" * 80 + "\n"
        for issue in high_activity[:3]:
            output += f"• {issue.key}: {issue.fields.summary}\n"
            output += f"  Comments: {len(issue.fields.comment.comments)}\n\n"
    
    if stale:
        output += "\n💤 STALE ISSUES (No Comments Yet):\n"
        output += "-" * 80 + "\n"
        for issue in stale[:3]:
            output += f"• {issue.key}: {issue.fields.summary}\n"
            output += f"  Status: {issue.fields.status.name}\n\n"
    
    output += "\n💡 Recommendations:\n"
    if blocked:
        output += "• Escalate blocked issues immediately\n"
    if high_activity:
        output += "• Review high-activity issues - may need PM intervention\n"
    if stale:
        output += "• Check in on stale issues - ensure they're not forgotten\n"
    
    return [TextContent(type="text", text=output)]


def format_executive(issue, analysis):
    """Format for executive audience"""
    
    priority = issue.fields.priority.name if hasattr(issue.fields, 'priority') and issue.fields.priority else 'Not set'
    assignee = issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned'
    
    return f"""**{issue.key}**: {issue.fields.summary}

Priority: {priority} | Status: {issue.fields.status.name} | Owner: {assignee}

{analysis}

**EXECUTIVE ACTIONS:**
☐ Review recommendations above
☐ Escalate blockers to appropriate teams
☐ Set follow-up checkpoint date"""


def format_technical(issue, comments, analysis):
    """Format for engineering audience"""
    
    priority = issue.fields.priority.name if hasattr(issue.fields, 'priority') and issue.fields.priority else 'Not set'
    assignee = issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned'
    
    # Find technical comments
    tech_keywords = ['code', 'api', 'database', 'error', 'config', 'patch', 'stack', 'query']
    tech_comments = [c for c in comments if any(kw in c.body.lower() for kw in tech_keywords)]
    
    output = f"""**{issue.key}**: {issue.fields.summary}

Status: {issue.fields.status.name} | Priority: {priority} | Assignee: {assignee}

{analysis}

**TECHNICAL CONTEXT:**
"""
    
    if tech_comments:
        for i, c in enumerate(tech_comments[:3], 1):
            excerpt = c.body[:200] + "..." if len(c.body) > 200 else c.body
            output += f"\n{i}. {c.author.displayName} ({c.created[:10]}):\n   {excerpt}\n"
    else:
        output += "No technical details in comments.\n"
    
    output += """
**IMPLEMENTATION CHECKLIST:**
☐ Review analysis recommendations
☐ Identify immediate workarounds
☐ Test in development environment
☐ Implement permanent solution
☐ Update documentation"""
    
    return output


def format_pm(issue, comments, analysis):
    """Format for PM audience"""
    
    priority = issue.fields.priority.name if hasattr(issue.fields, 'priority') and issue.fields.priority else 'Not set'
    assignee = issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned'
    comment_count = len(comments)
    
    engagement = "🔥 High activity" if comment_count > 5 else "📊 Moderate activity" if comment_count > 2 else "💤 Low activity"
    
    return f"""**{issue.key}**: {issue.fields.summary}

Status: {issue.fields.status.name} | Priority: {priority} | Owner: {assignee}
Discussion: {comment_count} comments | {engagement}

{analysis}

**TEAM COORDINATION:**
☐ Engineering review needed?
☐ Design input needed?
☐ QA planning needed?
☐ Dependencies on other issues?

**SPRINT PLANNING:**
☐ Keep in current sprint?
☐ Move to next sprint?
☐ Break into smaller stories?
☐ Escalate blockers?"""


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
