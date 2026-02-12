# JiraIQ MCP Server

**Turn Claude into your Jira analyst.** Analyze issues, find blockers, and generate stakeholder reports directly in Claude Desktop.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 🚀 What It Does

JiraIQ provides three powerful tools for Claude:

1. **analyze_jira_issue** - Analyze any Jira issue and get executive, technical, or PM reports
2. **find_blocked_issues** - Find all blocked issues in a project
3. **analyze_sprint** - Get sprint health analysis with blockers and risks

## ✨ Features

- 🎯 **Three Stakeholder Templates**: Executive summaries, technical analysis, and PM reports
- 🔍 **Smart Analysis**: Uses Claude AI to identify sentiment, blockers, and risks
- ⚡ **Fast**: Analyzes issues in seconds instead of manual 30-60 minute review
- 🔌 **MCP Integration**: Works directly in Claude Desktop chat
- 🏢 **Built for Oracle/ERP Teams**: Detects OIC, VBCS, Fusion, and other Oracle-specific issues

## 📋 Prerequisites

- Python 3.10 or higher
- [Claude Desktop](https://claude.ai/download)
- Jira Cloud or Server instance
- [Anthropic API key](https://console.anthropic.com/)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/jiraiq-mcp.git
cd jiraiq-mcp
```

### 2. Install Dependencies

```bash
pip install mcp jira anthropic python-dotenv
```

### 3. Configure Credentials

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your credentials
```

Fill in your `.env` file:

```bash
JIRA_URL=https://yourcompany.atlassian.net
JIRA_EMAIL=your.email@company.com
JIRA_TOKEN=your_jira_api_token
ANTHROPIC_API_KEY=your_anthropic_api_key
```

**Get your credentials:**
- **Jira API Token**: [Create here](https://id.atlassian.com/manage-profile/security/api-tokens)
- **Anthropic API Key**: [Create here](https://console.anthropic.com/)

### 4. Test Installation

```bash
# Test Jira connection
python test_jira.py

# Test Claude AI connection
python test_claude.py

# Test MCP server
python test_mcp.py
```

### 5. Configure Claude Desktop

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**Mac/Linux:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "jiraiq": {
      "command": "python",
      "args": ["C:\\FULL\\PATH\\TO\\jiraiq_server.py"],
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

**Important:** 
- Use the FULL absolute path to `jiraiq_server.py`
- Windows: Use double backslashes `C:\\Pratap\\work\\`
- Mac/Linux: Use forward slashes `/Users/pratap/projects/`

### 6. Restart Claude Desktop

Close and reopen Claude Desktop to load the MCP server.

## 🎯 Usage

### Analyze a Single Issue

```
User: Analyze Jira issue ENG-123 for executives

Claude: [Calls analyze_jira_issue tool and returns executive summary with 
         team sentiment, blockers, risks, and actionable recommendations]
```

### Get All Three Report Types

```
User: Analyze ENG-123 with all templates

Claude: [Generates executive, technical, and PM reports]
```

### Find Blocked Issues

```
User: Find all blocked issues in project ENG

Claude: [Returns list of blocked issues with details]
```

### Analyze Sprint Health

```
User: Analyze the current sprint for project ENG

Claude: [Returns sprint health report with blocked/active/stale issues]
```

### Advanced Usage

```
User: Analyze ENG-101, ENG-102, and ENG-103. Find common blockers 
      and create an escalation email for my VP.

Claude: [Combines multiple analyses and generates custom output]
```

## 📊 Available Templates

### 🎩 Executive Template
- **Audience:** Leadership, VPs, Directors
- **Format:** 30-second summary
- **Focus:** Business impact, risks, clear action items
- **Best for:** Reporting up to management

### 💻 Technical Template
- **Audience:** Engineers, Tech Leads
- **Format:** Implementation-ready analysis
- **Focus:** Technical context, code references, checklists
- **Best for:** Handing off to engineering teams

### 📋 PM Template
- **Audience:** Product Managers, Scrum Masters
- **Format:** Sprint planning focused
- **Focus:** Team coordination, sprint impact, stakeholder communication
- **Best for:** Sprint planning and team coordination

## 🔧 Troubleshooting

### "No tools available" in Claude Desktop

1. Verify `claude_desktop_config.json` has correct path
2. Check path uses absolute path (not relative)
3. Restart Claude Desktop completely
4. Check logs: `%APPDATA%\Claude\Logs` (Windows) or `~/Library/Logs/Claude/` (Mac)

### "Could not fetch issue"

1. Verify JIRA_URL is correct (no trailing slash)
2. Check JIRA_EMAIL matches your Atlassian account
3. Regenerate JIRA_TOKEN if needed
4. Verify you have access to the project/issue

### "Module not found: mcp"

Install dependencies for the correct Python version:

```bash
# Find which Python Claude Desktop uses
where python  # Windows
which python  # Mac/Linux

# Install for that specific Python
C:\Path\To\Python\python.exe -m pip install mcp jira anthropic python-dotenv
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Claude](https://claude.ai) by Anthropic
- Uses [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- Jira integration via [jira-python](https://github.com/pycontribs/jira)

## 📧 Support

- Create an [Issue](https://github.com/yourusername/jiraiq-mcp/issues)
- Connect on [LinkedIn](https://linkedin.com/in/yourprofile)

---

**Built by Pratap Yeragudipati** | Solving Jira analysis pain for Oracle/ERP implementation teams
