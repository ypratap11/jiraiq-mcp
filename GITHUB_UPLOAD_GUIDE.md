# GitHub Upload Guide for JiraIQ

## ✅ Files to Upload (Safe)

These files are SAFE to upload to public GitHub:

```
jiraiq-mcp/
├── .gitignore              ✅ UPLOAD (prevents future accidents)
├── .env.example            ✅ UPLOAD (template for others)
├── LICENSE                 ✅ UPLOAD (MIT license)
├── README.md               ✅ UPLOAD (use README_GITHUB.md)
├── pyproject.toml          ✅ UPLOAD (project config)
├── jiraiq_server.py        ✅ UPLOAD (main server code)
├── test_jira.py            ✅ UPLOAD (test script)
├── test_claude.py          ✅ UPLOAD (test script)
└── test_mcp.py             ✅ UPLOAD (test script)
```

## ❌ Files to NEVER Upload

These contain secrets or are unnecessary:

```
❌ .env                     DO NOT UPLOAD (your credentials!)
❌ __pycache__/             DO NOT UPLOAD (Python cache)
❌ .idea/                   DO NOT UPLOAD (PyCharm config)
❌ main.py                  DO NOT UPLOAD (PyCharm template)
❌ test_connection.py       OPTIONAL (just local testing)
```

## 🚀 Step-by-Step Upload Process

### Step 1: Clean Up Your Directory

**Delete unnecessary files:**

```powershell
cd C:\Pratap\work\jiraiq-mcp

# Delete PyCharm files
Remove-Item -Recurse -Force .idea
Remove-Item -Recurse -Force __pycache__
Remove-Item main.py

# Optional: Remove test_connection.py (it's redundant)
Remove-Item test_connection.py
```

### Step 2: Add the New Files

**Copy the files I just created:**

1. Download `.gitignore` (I just created it)
2. Download `LICENSE` (I just created it)
3. Download `README_GITHUB.md` (I just created it)

**Put them in your project:**

```powershell
# Save downloaded files to C:\Pratap\work\jiraiq-mcp\

# Rename README
Rename-Item README.md README_OLD.md
Rename-Item README_GITHUB.md README.md
```

### Step 3: Double-Check .env is NOT Included

```powershell
# View .gitignore to verify .env is excluded
type .gitignore

# You should see:
# .env
# .env.local
```

### Step 4: Initialize Git Repository

```powershell
cd C:\Pratap\work\jiraiq-mcp

# Initialize Git
git init

# Add .gitignore first (important!)
git add .gitignore
git commit -m "Add .gitignore"

# Add all files
git add .
git commit -m "Initial commit: JiraIQ MCP Server"
```

**Git will automatically ignore:**
- `.env` (your credentials)
- `__pycache__/`
- `.idea/`
- Any other files in `.gitignore`

### Step 5: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `jiraiq-mcp`
3. Description: "AI-powered Jira analysis MCP server for Claude Desktop"
4. Visibility: **Public** (to share) or **Private** (to keep secret)
5. **Do NOT** check "Add README" (you already have one)
6. Click "Create repository"

### Step 6: Push to GitHub

**Copy the commands GitHub shows you:**

```powershell
# Connect local repo to GitHub (replace with your username)
git remote add origin https://github.com/yourusername/jiraiq-mcp.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Enter your GitHub credentials when prompted.**

### Step 7: Verify on GitHub

1. Go to `https://github.com/yourusername/jiraiq-mcp`
2. **Check these files are PRESENT:**
   - ✅ README.md
   - ✅ jiraiq_server.py
   - ✅ .gitignore
   - ✅ LICENSE
   - ✅ pyproject.toml
   - ✅ test files

3. **Check these files are ABSENT:**
   - ❌ .env (should NOT be there!)
   - ❌ __pycache__
   - ❌ .idea

**If .env is there: DELETE THE REPO IMMEDIATELY and start over!**

## 🔒 Security Checklist

Before making repo public, verify:

- [ ] ✅ .env is NOT in the repo
- [ ] ✅ No API keys in any files
- [ ] ✅ No passwords in any files
- [ ] ✅ .gitignore is present
- [ ] ✅ README has no sensitive info
- [ ] ✅ No real Jira URLs in examples

## 📝 Update README Before Uploading

**Replace these placeholders in README.md:**

```markdown
# Replace with your actual username
https://github.com/yourusername/jiraiq-mcp

# Replace with your LinkedIn
https://linkedin.com/in/yourprofile
```

## 🎯 What Happens Next

Once on GitHub, people can:

1. **Clone your repo:**
   ```bash
   git clone https://github.com/yourusername/jiraiq-mcp.git
   ```

2. **Copy .env.example to .env:**
   ```bash
   cp .env.example .env
   ```

3. **Fill in their own credentials** in `.env`

4. **Run your MCP server** with their Jira!

## 💡 Pro Tips

### Make it Private First

If you're nervous, make it **private** first:
- Test everything works
- Share with 1-2 people
- Make public later

### Add a GitHub Actions Badge (Optional)

Add to README.md:
```markdown
[![GitHub stars](https://img.shields.io/github/stars/yourusername/jiraiq-mcp?style=social)](https://github.com/yourusername/jiraiq-mcp)
```

### Create Releases (Later)

Once stable, create v1.0.0 release:
1. Go to "Releases" on GitHub
2. Click "Create a new release"
3. Tag: `v1.0.0`
4. Title: "JiraIQ v1.0.0 - Initial Release"

## 🚨 Emergency: If You Uploaded .env

**If you accidentally uploaded your .env file:**

1. **Delete the repository immediately** on GitHub
2. **Regenerate ALL credentials:**
   - New Jira API token
   - New Anthropic API key
3. **Start fresh** with proper .gitignore
4. **Never** try to just "remove" the file - Git history keeps it!

## ✅ Final Checklist

Before pushing to GitHub:

- [ ] ✅ Cleaned up directory (no .idea, __pycache__)
- [ ] ✅ Added .gitignore
- [ ] ✅ Added LICENSE
- [ ] ✅ Updated README.md
- [ ] ✅ Verified .env is NOT staged (`git status`)
- [ ] ✅ Tested locally one more time
- [ ] ✅ Created GitHub repository
- [ ] ✅ Pushed code
- [ ] ✅ Verified .env is NOT on GitHub
- [ ] ✅ Updated README with your username/links

## 📧 Share the Repo

Once live, share it:

**On LinkedIn:**
```
Just open-sourced JiraIQ - an MCP server that turns Claude into a Jira analyst.

Analyzes issues in 30 seconds, generates executive/technical/PM reports.

Built for Oracle/ERP implementation teams.

Repo: https://github.com/yourusername/jiraiq-mcp

#OpenSource #BuildInPublic #Claude #MCP
```

**In your Tuesday launch post:**
```
Code is open source: https://github.com/yourusername/jiraiq-mcp

Try it yourself or customize for your team.
```

---

**You're ready to upload!** 🚀

Just follow the steps above and you'll have a professional GitHub repo.

Let me know when you've uploaded and I'll check it with you!
