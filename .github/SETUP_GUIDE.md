# Repository Setup Guide

This guide walks through setting up branch protection, GitHub features, and repository configuration for Phola Park App.

## 1. Enable GitHub Features

### Enable Discussions
1. Go to **Settings** → **General**
2. Scroll to "Features"
3. ✅ Check **Discussions**
4. Click **Save**

**Benefits:**
- Q&A section for contributors
- Announcements for releases
- Show & tell for community

### Enable GitHub Projects
1. Go to **Settings** → **General**
2. Check **Projects** (should be enabled by default)
3. Go to **Projects** tab to create your first board

**Suggested Project Boards:**
- 🚀 **Product Roadmap** - Future features and milestones
- 🐛 **Bug Backlog** - Issues to fix
- 📋 **In Development** - Current work
- ✅ **Ready for Review** - PRs waiting for review

---

## 2. Branch Protection Rules

### Enable Main Branch Protection

**Step 1: Access Branch Settings**
1. Go to **Settings** → **Branches**
2. Click **Add rule** under "Branch protection rules"
3. Enter `main` in the "Branch name pattern" field

**Step 2: Configure Protection Rules**

✅ **Require a pull request before merging**
- ✅ Require approvals: **1** (or more)
- ✅ Require review from code owners
- ✅ Allow auto-merge (optional, recommended)
- ✅ Require branches to be up to date before merging

✅ **Require status checks to pass before merging**
- ✅ Require branches to be up to date
- ✅ Select: `build` and `test` (from GitHub Actions)

✅ **Require signed commits** (optional but recommended)
- ✅ Require commits to be signed

✅ **Restrict who can push to matching branches**
- Include administrators (recommended for larger teams)

✅ **Other Protection Settings**
- ✅ Allow force pushes: **Nobody**
- ✅ Allow deletions: **No**
- ✅ Dismiss stale pull request approvals: **Yes**
- ✅ Require conversation resolution: **Yes**
- ✅ Require linear history: **No** (optional)

**Step 3: Save Rule**
- Click **Create** to apply the rule

---

## 3. Create GitHub Labels

Use this script to create labels programmatically or manually create them:

### Manual Label Creation
1. Go to **Issues** → **Labels**
2. Click **New label**
3. Create each label with name, description, and color

### Labels to Create

**Priority Labels:**
```
Priority: Critical     | #FF0000 (Red)
Priority: High         | #FF6600 (Orange)
Priority: Medium       | #FFCC00 (Yellow)
Priority: Low          | #99CCFF (Light Blue)
```

**Type Labels:**
```
type: bug              | #D73A49 (Red)
type: feature          | #0366D6 (Blue)
type: enhancement      | #A2EEEF (Cyan)
type: documentation    | #0075CA (Dark Blue)
type: chore            | #CCCCCC (Gray)
type: refactor         | #7B3FF2 (Purple)
```

**Status Labels:**
```
status: backlog        | #FBCA04 (Yellow)
status: in-progress    | #FFC900 (Gold)
status: in-review      | #0366D6 (Blue)
status: blocked        | #D73A49 (Red)
status: on-hold        | #999999 (Gray)
status: done           | #28A745 (Green)
```

**Area Labels:**
```
area: auth             | #D4C5F9 (Light Purple)
area: api              | #5DADE2 (Light Blue)
area: database         | #145A32 (Dark Green)
area: ui               | #E8B4B8 (Light Pink)
area: notifications    | #F39C12 (Orange)
area: reports          | #2E86C1 (Blue)
area: surveys          | #1ABC9C (Teal)
```

**Other Labels:**
```
good first issue       | #7057FF (Purple)
help wanted            | #33AA3F (Green)
question               | #D876E3 (Magenta)
duplicate              | #CCCCCC (Gray)
wontfix                | #FFFFFF (White)
security               | #D73A49 (Red)
performance            | #FFA500 (Orange)
```

---

## 4. Create GitHub Milestones

1. Go to **Issues** → **Milestones**
2. Click **New milestone** for each version

### Suggested Milestones
```
Version: v1.0.0 Release    (Due: TBD)
Version: v1.1.0 Enhancements
Version: v2.0.0 Major Features
Backlog: Future Features
Backlog: Technical Debt
```

---

## 5. Create GitHub Projects

### Project 1: Product Roadmap
1. Go to **Projects** → **New project**
2. Choose **Table** or **Board** template
3. Name: "Product Roadmap"
4. Add custom fields for priority, status, ETA
5. Add issues for planned features

### Project 2: Bug Backlog
1. Create new project: "Bug Backlog"
2. Add columns: **Reported** → **Confirmed** → **Assigned** → **Fixed**
3. Add all open bug issues

### Project 3: Development Sprint
1. Create new project: "Current Sprint"
2. Add columns: **Todo** → **In Progress** → **In Review** → **Done**
3. Limit WIP per column for better flow

---

## 6. Configure Issue Settings

1. Go to **Settings** → **General**
2. Under "Merge button":
   - Allow squash merging: ✅
   - Allow rebase merging: ✅
   - Allow auto-merge: ✅
3. Default merge message: `PR_TITLE`
4. Default commit title: `MERGE_MESSAGE`

---

## 7. Enable GitHub Wiki (Optional)

1. Go to **Settings** → **General**
2. Check **Wikis** under Features
3. Add documentation pages:
   - Home
   - API Documentation
   - Database Schema
   - Deployment Guide
   - Troubleshooting

---

## 8. Configure Notifications

1. Go to **Settings** → **Notifications**
2. Default branch notification: **Watching**
3. Enable email notifications for:
   - PR reviews requested
   - Issues assigned to you
   - Mentions
   - Security vulnerabilities

---

## 9. Add Repository Topics

1. Go to **Settings** → **General**
2. Scroll to "Topics"
3. Add relevant topics:
   - `flask`
   - `python`
   - `web-app`
   - `community-management`
   - `role-based-access`
   - `incident-reporting`
   - `survey-management`

---

## 10. Create Webhook (Optional)

For integrations with CI/CD or external services:

1. Go to **Settings** → **Webhooks**
2. Click **Add webhook**
3. Configure for your needs (Slack, Discord, custom servers)

---

## Verification Checklist

After setup, verify:

- [ ] Branch protection enabled on `main`
- [ ] PR template working (create new PR to test)
- [ ] Issue templates available (create new issue)
- [ ] All labels created
- [ ] Milestones created and linked to issues
- [ ] Projects created and populated
- [ ] GitHub Actions workflow running
- [ ] CODEOWNERS file configured
- [ ] Discussions enabled
- [ ] Topics added to repository

---

## Quick Reference

| Setting | Status |
|---------|--------|
| **Documentation** | ✅ Complete (README, CONTRIBUTING, etc.) |
| **Templates** | ✅ Complete (PR, Issue templates) |
| **CI/CD** | ✅ Complete (GitHub Actions) |
| **Code Ownership** | ✅ Complete (CODEOWNERS) |
| **Branch Protection** | ⏳ Needs Manual Setup |
| **Labels** | ⏳ Needs Manual Setup |
| **Milestones** | ⏳ Needs Manual Setup |
| **Projects** | ⏳ Needs Manual Setup |

---

## Getting Help

- **GitHub Docs**: https://docs.github.com
- **Branch Protection**: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches
- **Issues & PRs**: https://docs.github.com/en/issues
- **Projects**: https://docs.github.com/en/issues/planning-and-tracking-with-projects

---

**Last Updated**: August 17, 2026
