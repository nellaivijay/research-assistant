# Wiki Pages Setup Guide

Complete guide for setting up and managing GitHub Wiki pages for the Enhanced Research Assistant.

## 📋 Table of Contents

1. [GitHub Wiki Overview](#github-wiki-overview)
2. [Wiki Structure](#wiki-structure)
3. [Wiki Setup](#wiki-setup)
4. [Wiki Management](#wiki-management)
5. **Wiki Best Practices**](#wiki-best-practices)
6. [Wiki SEO](#wiki-seo)
7. [Wiki Maintenance](#wiki-maintenance)

## GitHub Wiki Overview

GitHub Wiki is a simple way to provide documentation for your project directly in the repository.

### Benefits for Research Assistant

- **Integrated Documentation**: Documentation lives with code
- **Easy Editing**: Web-based editor
- **Version Control**: Changes tracked in git
- **Collaborative**: Multiple contributors
- **Searchable**: GitHub search integration
- **Markdown Support**: Simple formatting

### Wiki vs GitHub Pages

| Feature | GitHub Wiki | GitHub Pages |
|---------|-------------|--------------|
| **Editing** | Web-based editor | Requires git commits |
| **Structure** | Flat page list | Hierarchical site |
| **Versioning** | Per-page history | Git-based history |
| **SEO** | Basic | Full SEO control |
| **Customization** | Limited | Full customization |
| **Use Case** | Documentation | Marketing website |

## Wiki Structure

### Current Wiki Structure

```
research-assistant/
├── wiki/
│   ├── _Home.md              # Wiki home page
│   ├── Getting-Started.md     # Quick start guide
│   ├── User-Guide.md          # Complete user manual
│   ├── System-Architecture.md # System documentation
│   ├── Solution-Design.md     # Solution approach
│   ├── Technical-Documentation.md # Developer docs
│   ├── Installation-Guide.md  # Installation instructions
│   ├── Build-Process.md       # Build process documentation
│   ├── Deployment-Guide.md    # Deployment instructions
│   ├── GitHub-Pages-Setup.md  # GitHub Pages setup
│   ├── SEO-Guide.md           # SEO optimization
│   └── Wiki-Pages-Setup.md    # This file
```

### Wiki Page Organization

**Categories:**
- **User Documentation**: Getting Started, User Guide
- **Developer Documentation**: Technical Documentation, Build Process
- **Architecture Documentation**: System Architecture, Solution Design
- **Operations Documentation**: Installation Guide, Deployment Guide
- **Setup Documentation**: GitHub Pages Setup, Wiki Pages Setup
- **Optimization Documentation**: SEO Guide

## Wiki Setup

### Method 1: Automatic Setup (Recommended)

#### Step 1: Create Wiki Directory

```bash
cd /home/ramdov/projects/research-assistant
mkdir -p wiki
```

#### Step 2: Create Wiki Pages

Create Markdown files in the `wiki/` directory:

```bash
# Create wiki home page
touch wiki/_Home.md

# Create documentation pages
touch wiki/Getting-Started.md
touch wiki/User-Guide.md
# ... add more pages
```

#### Step 3: Enable Wiki

1. Go to repository on GitHub
2. Click "Wiki" tab
3. Wiki will be automatically populated with files from `wiki/` directory
4. Pages can be edited directly on GitHub

### Method 2: Manual Setup

#### Step 1: Enable Wiki

1. Go to repository Settings
2. Scroll down to "Features"
3. Click "Wikis"
4. Click "Set up a wiki"

#### Step 2: Create Pages

1. Click "New Page"
2. Enter page name
3. Write content in Markdown
4. Click "Save page"

#### Step 3. Organize Pages

1. Click "Add sidebar"
2. Add pages to sidebar
3. Organize by category
4. Save sidebar

## Wiki Management

### Creating New Pages

**Via GitHub Web Interface:**

1. Go to repository Wiki tab
2. Click "New Page"
3. Enter page name (use hyphens for spaces)
4. Write content in Markdown
5. Add optional summary
5. Click "Save page"

**Via Git:**

```bash
# Create new wiki page
cd wiki
touch New-Page-Name.md

# Add content
echo "# New Page Title" > New-Page-Name.md
echo "Page content..." >> New-Page-Markdown

# Commit and push
git add wiki/New-Page-Name.md
git commit -m "Add new wiki page"
git push github main
```

### Editing Pages

**Via GitHub Web Interface:**

1. Go to repository Wiki tab
2. Click on page to edit
3. Make changes using Markdown editor
4. Click "Save page"

**Via Git:**

```bash
# Edit wiki page
nano wiki/Existing-Page.md

# Commit and push
git add wiki/Existing-Page.md
git commit -m "Update wiki page"
git push github main
```

### Page Organization

**Sidebar Organization:**

1. Go to Wiki tab
2. Click "Add sidebar"
3. Create categories:
   - User Documentation
   - Developer Documentation
   - Architecture Documentation
   - Operations Documentation
4. Add pages to appropriate categories
5. Save sidebar

**Page Hierarchy:**

**Flat Structure (Current):**
```
Home
├── Getting Started
├── User Guide
├── System Architecture
└── ...
```

**Hierarchical Structure:**
```
Home
├── Documentation
│   ├── Getting Started
│   ├── User Guide
│   └── ...
└── Development
    ├── Technical Documentation
    ├── Build Process
    └── ...
```

### Deleting Pages

**Via GitHub Web Interface:**

1. Go to repository Wiki tab
2. Click on page to delete
3. Click "Delete page"
4. Confirm deletion

**Via Git:**

```bash
# Delete wiki page
rm wiki/Unwanted-Page.md

# Commit and push
git add wiki/Unwanted-Page.md
git commit -m "Remove wiki page"
git push github main
```

## Wiki Best Practices

### Content Guidelines

**Writing Style:**
- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Use consistent formatting
- Update content regularly

**Page Structure:**

```markdown
# Page Title

Brief description of what this page covers.

## Section 1

Content for section 1.

## Section 2

Content for section 2.

## Related Pages

- [Related Page 1](Related-Page-1.md)
- [Related Page 2](Related-Page-2.md)
```

### Markdown Formatting

**Common Elements:**

```markdown
# Heading 1
## Heading 2
### Heading 3

**Bold text**
*Italic text*
`Code inline`

```python
# Code block
def function():
    pass
```

- List item 1
- List item 2

1. Numbered item
2. Numbered item

[Link text](URL)
![Alt text](image-url)

> Blockquote

---
```

### Linking Between Pages

**Internal Links:**
```markdown
[Getting Started](Getting-Started.md)
[User Guide](User-Guide.md)
```

**External Links:**
```markdown
[GitHub Repository](https://github.com/nellaivijay/research-assistant)
[Live Application](https://huggingface.co/spaces/nellaivijay/research-assistant)
```

### Code Examples

**Including Code:**

```markdown
## Installation

```bash
git clone https://github.com/nellaivijay/research-assistant.git
cd research-assistant
pip install -r requirements.txt
```

## Running the Application

```python
python app.py
```
```

## Wiki SEO

### Wiki Search Optimization

**GitHub Wiki SEO:**
- GitHub wikis are searchable
- Page titles appear in search results
- Content is indexed by search engines

**Wiki SEO Best Practices:**

**Title Optimization:**
- Use descriptive page titles
- Include primary keywords
- Keep titles concise

**Content Optimization:**
- Include keywords naturally
- Use heading structure
- Add internal links
- Update content regularly

**Internal Linking:**
```markdown
See [Installation Guide](Installation-Guide.md) for setup instructions.
For deployment details, see [Deployment Guide](Deployment-Guide.md).
```

### Cross-Linking

**Link to GitHub Pages:**
```markdown
For the full documentation site, see [GitHub Pages](https://nellaivijay.github.io/research-assistant)
```

**Link to Repository:**
```markdown
Source code available at [GitHub Repository](https://github.com/nellaivijay/research-assistant)
```

**Link to Live Application:**
```markdown
Try the live application at [Hugging Face Spaces](https://huggingface.co/spaces/nellaivijay/research-assistant)
```

## Wiki Maintenance

### Regular Maintenance Tasks

**Weekly:**
- Review recent changes
- Check for broken links
- Update outdated information
- Respond to user questions

**Monthly:**
- Content audit
- Update based on features
- Add new documentation
- Reorganize if needed

**Quarterly:**
- Comprehensive review
- Restructure if needed
- Update navigation
- SEO review

### Content Updates

**Update Triggers:**
- New features added
- User feedback received
- Documentation gaps identified
- SEO performance data
- Platform changes

**Update Process:**
1. Identify page to update
2. Make necessary changes
3. Review for consistency
4. Commit and push changes
5. Verify on GitHub

### Version Control

**Wiki History:**
- Each page has full edit history
- Compare different versions
- Revert changes if needed
- Track who made changes

**Viewing History:**
1. Go to Wiki page
2. Click "Revisions"
3. View version history
4. Compare versions
5. Revert if needed

### Collaboration

**Multiple Contributors:**
- Wiki supports multiple contributors
- Edit conflicts are resolved in web interface
- Track contributions via page history
- Discuss changes in page comments

**Guidelines for Contributors:**
- Follow existing style and structure
- Add meaningful content
- Update table of contents
- Link to related pages
- Test formatting before saving

## Advanced Wiki Features

### Page Permissions

**Repository Permissions:**
- **Public repositories**: Anyone can edit wiki
- **Private repositories**: Only collaborators can edit
- **Organization repositories**: Organization members can edit

**Page Restrictions:**
- Set wiki access levels in repository settings
- Restrict editing to specific collaborators
- Enable/disable wiki entirely

### Wiki Cloning

**Clone Wiki Repository:**
```bash
# Clone wiki as git repository
git clone https://github.com/nellaivijay/research-assistant.wiki.git
```

**Edit Locally:**
```bash
cd research-assistant.wiki
# Edit pages locally
git add .
git commit -m "Update wiki"
git push
```

### Wiki Export

**Export to PDF:**
1. Go to Wiki page
2. Click "Export to PDF"
3. Download PDF file

**Export to Markdown:**
1. Go to Wiki page
2. Click "Raw"
3. Copy Markdown content
4. Save as .md file

### Wiki Statistics

**Page Analytics:**
- View count per page
- Edit history
- Contributor information
- Recent changes

**Access via GitHub:**
1. Go to repository Insights
2. View wiki statistics
3. Track page popularity

## Wiki vs Documentation Files

### When to Use Wiki

**Use GitHub Wiki for:**
- Quick documentation
- User guides
- FAQ pages
- Troubleshooting guides
- Release notes
- Contributing guidelines

**Use Documentation Files for:**
- Comprehensive technical documentation
- API references
- Architecture documentation
- Marketing content
- Tutorial series

### Hybrid Approach

**Current Implementation:**
- **Wiki**: User-facing documentation
- **Documentation Files**: Developer documentation
- **GitHub Pages**: Professional documentation site

**Benefits:**
- Wiki for easy updates
- Docs for technical depth
- GitHub Pages for presentation

## Wiki Backup and Migration

### Backup Strategy

**Automatic Backup:**
- Wiki is backed up with repository
- Full page history preserved
- Can revert any changes

**Manual Backup:**
```bash
# Clone wiki repository
git clone https://github.com/nellaivijay/research-assistant.wiki.git wiki-backup
```

### Migration

**Export to Other Platforms:**
- Export pages as Markdown
- Convert to other formats
- Import to Confluence
- Import to Notion
- Import to GitBook

---

**For more information, visit the [GitHub Repository](https://github.com/nellaivijay/research-assistant)**