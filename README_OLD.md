# JiraIQ MCP Server

**Turn Claude into your Jira analyst.** Analyze issues, find blockers, and generate stakeholder reports directly in your Claude chat.

## What It Does

JiraIQ provides three powerful tools for Claude:

1. **analyze_jira_issue** - Analyze any Jira issue and get executive, technical, or PM reports
2. **find_blocked_issues** - Find all blocked issues in a project
3. **analyze_sprint** - Get sprint health analysis with blockers and risks

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Claude Desktop app (download from claude.ai)
- Jira Cloud or Server instance
- Anthropic API key

### Installation (5 minutes)

#### Step 1: Install Dependencies

```bash
# Install MCP SDK
pip install mcp

# Install JiraIQ dependencies
pip install jira anthropic python-dotenv
```

#### Step 2: Set Up Configuration

Create a `.env` file with your credentials:

```bash
# Jira Configuration
JIRA_URL=https://yourcompany.atlassian.net
JIRA_EMAIL=your.email@company.com
JIRA_TOKEN=your_jira_api_token

# Anthropic API
ANTHROPIC_API_KEY=your_anthropic_api_key
```

**Getting your credentials:**

- **Jira API Token**: Go to https://id.atlassian.com/manage-profile/security/api-tokens → Create API token
- **Anthropic API Key**: Go to https://console.anthropic.com/ → API Keys → Create key

#### Step 3: Configure Claude Desktop

Add JiraIQ to your Claude Desktop config:

**On Mac/Linux:** `~/Library/Application\ Support/Claude/claude_desktop_config.json`

**On Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "jiraiq": {
      "command": "python",
      "args": ["path/to/jiraiq_server.py"],
      "env": {
        "JIRA_URL": "https://yourcompany.atlassian.net",
        "JIRA_EMAIL": "your.email@company.com",
        "JIRA_TOKEN": "your_jira_token",
        "ANTHROPIC_API_KEY": "your_anthropic_key"
      }
    }
  }
}
```

**Replace `path/to/jiraiq_server.py` with the actual path!**

#### Step 4: Restart Claude Desktop

Close and reopen Claude Desktop to load the MCP server.

---

## Usage

### Analyze a Single Issue

```
User: Analyze Jira issue ENG-123 for executives

Claude: [calls analyze_jira_issue tool]
        
        EXECUTIVE SUMMARY: ENG-123
        
        Team Sentiment: Negative
        Blocker: Engineering blocked by procurement and finance
        Risk: Cross-functional dependency paralysis
        
        Recommendation: Schedule cross-functional sync within 48 hours...
```

### Get All Three Reports

```
User: Analyze ENG-123 with all templates

Claude: [generates executive, technical, and PM reports]
```

### Find Blocked Issues

```
User: Find all blocked issues in project ENG

Claude: [calls find_blocked_issues tool]
        
        🚨 Found 3 blocked issues in ENG:
        
        1. ENG-101: Oracle integration failing
           Status: Blocked | Priority: High
        ...
```

### Analyze Sprint Health

```
User: Analyze the current sprint for project ENG

Claude: [calls analyze_sprint tool]
        
        📊 SPRINT HEALTH REPORT: ENG
        
        Total Issues: 15
        Blocked: 2 🔴
        High Activity: 3 🟡
        Stale: 1 💤
        ...
```

---

## Available Templates

### Executive Template
- **Audience:** Leadership, VPs, Directors
- **Format:** 30-second summary
- **Focus:** Business impact, risks, next steps
- **Use when:** Reporting to management

### Technical Template
- **Audience:** Engineers, Tech Leads
- **Format:** Implementation-ready analysis
- **Focus:** Technical context, code refs, checklists
- **Use when:** Handing off to engineering

### PM Template
- **Audience:** Product Managers, Scrum Masters
- **Format:** Sprint planning focused
- **Focus:** Team coordination, sprint impact
- **Use when:** Planning sprints, coordinating teams

---

## Advanced Usage

### Custom Prompts

You can combine JiraIQ tools with custom prompts:

```
User: Analyze ENG-101, ENG-102, and ENG-103. 
      Find common blockers across all three and 
      create an escalation email for my VP.
```

### Batch Analysis

```
User: Find all blocked issues in ENG, then analyze 
      each one with the executive template and 
      create a summary report.
```

### Integration with Other Tools

JiraIQ works alongside other MCP servers. Example:

```
User: Analyze ENG-123, then create a Slack message 
      for the engineering channel summarizing the blocker.
```

---

## Troubleshooting

### "No tools available"

**Problem:** Claude doesn't see JiraIQ tools

**Solutions:**
1. Verify `claude_desktop_config.json` is in the correct location
2. Check that the path to `jiraiq_server.py` is absolute and correct
3. Restart Claude Desktop completely
4. Check Claude Desktop logs: `~/Library/Logs/Claude/mcp*.log` (Mac)

### "Could not fetch issue X"

**Problem:** Jira authentication failed

**Solutions:**
1. Verify JIRA_URL is correct (no trailing slash)
2. Regenerate your Jira API token
3. Verify you have access to the project/issue
4. Check JIRA_EMAIL matches your Atlassian account

### "ANTHROPIC_API_KEY not found"

**Problem:** API key not set in environment

**Solutions:**
1. Verify the key is in your `.env` file
2. Check `claude_desktop_config.json` includes the env variables
3. Restart Claude Desktop after adding the key

### MCP Server Crashes

**Check logs:**

Mac: `~/Library/Logs/Claude/mcp-server-jiraiq.log`
Windows: `%APPDATA%\Claude\Logs\mcp-server-jiraiq.log`

Common issues:
- Missing Python dependencies → Run `pip install -r requirements.txt`
- Python version too old → Upgrade to Python 3.10+
- Jira credentials invalid → Regenerate API token

---

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black jiraiq_server.py
```

### Type Checking

```bash
mypy jiraiq_server.py
```

---

## Security

- API keys are stored locally in your Claude Desktop config
- No data is sent to external servers except:
  - Jira API (for fetching issues)
  - Anthropic API (for analysis)
- Comments and issue data are not persisted

---

## Pricing

### Free Tier
- 50 issue analyses per month
- All templates
- Community support

### Pro ($49/month)
- 500 issue analyses per month
- Priority support
- Advanced features

### Enterprise ($499/month)
- Unlimited analyses
- Custom templates
- Private deployment
- SLA support

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## Support

- **Documentation:** https://github.com/pyeragudipati/jiraiq-mcp
- **Issues:** https://github.com/pyeragudipati/jiraiq-mcp/issues
- **Email:** pratap@jiraiq.com

---

## License

MIT License - see LICENSE file for details

---

## Changelog

### v1.0.0 (2026-02-06)
- Initial release
- Three core tools: analyze_issue, find_blocked, analyze_sprint
- Three templates: executive, technical, PM
- Oracle/ERP keyword detection
