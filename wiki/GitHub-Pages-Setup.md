# GitHub Pages Setup Guide

Complete guide for setting up GitHub Pages for the Enhanced Research Assistant documentation site.

## 📋 Table of Contents

1. [GitHub Pages Overview](#github-pages-overview)
2. [Initial Setup](#initial-setup)
3. [Automatic Deployment](#automatic-deployment)
4. [Custom Domain Setup](#custom-domain-setup)
5. **Advanced Configuration**](#advanced-configuration)
6. [Troubleshooting](#troubleshooting)
7. **Best Practices**](#best-practices)

## GitHub Pages Overview

GitHub Pages is a static site hosting service that takes HTML, CSS, and JavaScript files from a repository and publishes them as a website.

### Benefits for Research Assistant

- **Free Hosting**: No cost for documentation hosting
- **Custom Domain**: Option to use custom domain
- **HTTPS**: Automatic SSL certificates
- **CDN**: Global content delivery network
- **Version Control**: Git-based deployment
- **Automatic Deployment**: CI/CD integration

### Site Structure

```
research-assistant/
├── docs/                    # GitHub Pages source
│   ├── index.html          # Main documentation page
│   ├── assets/              # Images, CSS, JS (optional)
│   └── subpages/            # Additional pages (optional)
├── .github/workflows/
│   └── docs-deploy.yml     # Deployment workflow
└── README.md
```

## Initial Setup

### Step 1: Create Documentation Directory

```bash
cd /home/ramdov/projects/research-assistant
mkdir -p docs
```

### Step 2: Create Documentation Files

Create `docs/index.html` with your documentation content. The current implementation includes:

- Professional landing page
- Feature showcase
- SEO optimization
- Responsive design

### Step 3: Verify File Structure

```bash
# Verify docs directory exists
ls -la docs/

# Verify index.html exists
ls docs/index.html
```

## Automatic Deployment

### Step 1: Enable GitHub Pages

1. Go to repository Settings → Pages
2. Under "Build and deployment"
3. Select **Source**: "GitHub Actions"
4. Click **Save**

### Step 2: Configure Deployment Workflow

The `.github/workflows/docs-deploy.yml` workflow handles automatic deployment:

```yaml
name: Deploy Documentation to GitHub Pages

on:
  push:
    branches: [ main ]
    paths:
      - 'docs/**'
      - '.github/workflows/docs-deploy.yml'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './docs'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Step 3: Trigger Deployment

The workflow triggers automatically when:
- Files in `docs/` directory are pushed
- The workflow file is modified
- Manual trigger via GitHub Actions UI

### Step 4: Verify Deployment

1. Go to repository Actions tab
2. Look for "Deploy Documentation to GitHub Pages" workflow
3. Verify workflow shows green checkmark
4. Visit your GitHub Pages site

## Custom Domain Setup

### Step 1: Choose Custom Domain

1. Purchase domain from registrar (e.g., Namecheap, GoDaddy)
2. Or use subdomain (e.g., docs.yourdomain.com)

### Step 2: Configure DNS

**DNS Configuration:**
```
Type: CNAME
Name: docs (or your subdomain)
Value: nellaivijay.github.io
```

### Step 3: Configure GitHub Pages

1. Go to repository Settings → Pages
2. Under "Custom domain"
3. Add your custom domain
4. Click **Save**

### Step 4. Verify DNS Propagation

```bash
# Check DNS propagation
dig docs.yourdomain.com +short
# Should point to GitHub Pages IP
```

### Step 5. Enforce HTTPS

1. In GitHub Pages settings
2. Check "Enforce HTTPS"
3. GitHub will generate SSL certificate automatically

## Advanced Configuration

### Custom 404 Page

Create `docs/404.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Page Not Found</title>
</head>
<body>
    <h1>404 - Page Not Found</h1>
    <p>The page you're looking for doesn't exist.</p>
    <a href="/">Return to Home</a>
</body>
</html>
```

### Custom Theme

**Using Jekyll (Optional):**

1. Create `_config.yml` in docs directory:
```yaml
theme: minima
title: Research Assistant Documentation
description: AI-powered research companion
```

2. Add Jekyll front matter to HTML files:
```yaml
---
layout: default
title: Home
---
```

### Navigation Menu

Add navigation to `docs/index.html`:

```html
<nav>
    <a href="/">Home</a>
    <a href="/installation">Installation</a>
    <a href="/deployment">Deployment</a>
    <a href="https://github.com/nellaivijay/research-assistant">GitHub</a>
</nav>
```

### Multi-Page Documentation

Create additional pages:

```bash
# Create additional pages
touch docs/installation.html
touch docs/deployment.html
touch docs/api-reference.html
```

Add navigation between pages:

```html
<!-- In each page -->
<div class="sidebar">
    <h3>Documentation</h3>
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/installation.html">Installation</a></li>
        <li><a href="/deployment.html">Deployment</a></li>
    </ul>
</div>
```

## Troubleshooting

### Common Issues

#### Page Not Updating

**Problem**: Changes not reflected on GitHub Pages

**Solutions**:
```bash
# 1. Check workflow status
# Go to Actions tab and verify workflow ran

# 2. Clear cache
# GitHub Pages may take up to 10 minutes to update

# 3. Check file paths
# Ensure files are in docs/ directory

# 4. Verify workflow file
# Check docs-deploy.yml is in .github/workflows/
```

#### Build Failures

**Problem**: Deployment workflow failing

**Solutions**:
```bash
# 1. Check workflow logs
# Go to Actions → Click on failed workflow → Check logs

# 2. Verify file permissions
# Ensure docs/ directory has correct permissions

# 3. Check for large files
# GitHub Pages has 100MB file size limit

# 4. Verify workflow syntax
# Check YAML syntax in docs-deploy.yml
```

#### Custom Domain Issues

**Problem**: Custom domain not working

**Solutions**:
```bash
# 1. Check DNS propagation
dig yourdomain.com +short

# 2. Verify DNS configuration
# Ensure CNAME record points to GitHub Pages

# 3. Check HTTPS enforcement
# May take time for SSL certificate to generate

# 4. Check GitHub Pages settings
# Verify domain is correctly configured
```

#### 404 Errors

**Problem**: Pages returning 404 errors

**Solutions**:
```bash
# 1. Check file names
# Ensure files use lowercase and no spaces

# 2. Verify file locations
# Ensure files are in docs/ directory

# 3. Check case sensitivity
# GitHub Pages is case-sensitive

# 4. Clear browser cache
# Try hard refresh: Ctrl+Shift+R
```

## Best Practices

### File Organization

**Recommended Structure:**
```
docs/
├── index.html          # Main landing page
├── assets/             # Images, CSS, JS
│   ├── images/
│   ├── css/
│   └── js/
├── installation.html   # Installation guide
├── deployment.html    # Deployment guide
└── api-reference.html  # API documentation
```

### Performance Optimization

**Optimization Techniques:**
- Minify CSS and JavaScript
- Optimize images (compress, use WebP)
- Use lazy loading for images
- Enable browser caching
- Use CDN for static assets

### SEO Optimization

**Best Practices:**
- Use semantic HTML
- Add meta descriptions
- Include Open Graph tags
- Use descriptive URLs
- Add structured data
- Create sitemap.xml

### Accessibility

**Accessibility Features:**
- Use semantic HTML
- Add alt text to images
- Ensure color contrast
- Use ARIA labels
- Keyboard navigation support
- Screen reader friendly

### Version Control

**Git Workflow:**
```bash
# Create feature branch for documentation updates
git checkout -b docs-update

# Make changes
# Edit files in docs/

# Commit changes
git add docs/
git commit -m "Update documentation"

# Push and create PR
git push origin docs-update
```

### Monitoring

**Monitor GitHub Pages:**
- Check repository Settings → Pages for deployment status
- Monitor Actions tab for workflow runs
- Check site analytics (if enabled)
- Monitor for broken links

### Backup Strategy

**Backup Documentation:**
```bash
# Backup docs directory
cp -r docs docs.backup

# Commit backup to repository
git add docs.backup
git commit -m "Backup documentation"
```

---

**For more information, visit the [GitHub Repository](https://github.com/nellaivijay/research-assistant)**