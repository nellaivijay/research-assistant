# Deployment Guide

Complete guide for deploying the Enhanced Research Assistant to various platforms.

## 📋 Table of Contents

1. [Deployment Overview](#deployment-overview)
2. [Hugging Face Spaces Deployment](#hugging-face-spaces-deployment)
3. [GitHub Pages Deployment](#github-pages-deployment)
4. [Manual Deployment](#manual-deployment)
5. [CI/CD Deployment](#cicd-deployment)
6. [Environment Configuration](#environment-configuration)
7. [Deployment Verification](#deployment-verification)
8. [Rollback Procedures](#rollback-procedures)

## Deployment Overview

The Enhanced Research Assistant can be deployed to multiple platforms:

### Deployment Options

| Platform | Type | Automation | Difficulty |
|----------|------|------------|------------|
| Hugging Face Spaces | Cloud | CI/CD/Manual | Easy |
| GitHub Pages | Static | CI/CD/Manual | Easy |
| Self-hosted | On-prem | Manual | Medium |
| Docker | Container | Manual | Medium |

### Deployment Architecture

```
Developer → GitHub → CI/CD Pipeline → Multiple Platforms
                      ↓
                Hugging Face Spaces
                      ↓
                GitHub Pages
                      ↓
                Self-hosted (optional)
```

## Hugging Face Spaces Deployment

### Method 1: Git Deployment (Recommended)

#### Step 1: Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose:
   - **Space name**: `research-assistant`
   - **License**: MIT
   - **SDK**: Gradio
   - **Python version**: 3.10
4. Click "Create Space"

#### Step 2: Configure Git Remote

```bash
cd /home/ramdov/projects/research-assistant

# Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/nellaivijay/research-assistant.git

# Or update existing remote
git remote set-url hf https://huggingface.co/spaces/nellaivijay/research-assistant.git
```

#### Step 3: Deploy

```bash
# Push to Hugging Face
git push hf main
```

### Method 2: Web Interface Deployment

#### Step 1: Access Space Files

1. Go to your Space: https://huggingface.co/spaces/nellaivijay/research-assistant
2. Click "Files" tab
3. Click "Upload files"

#### Step 2: Upload Files

Upload these files:
- `app.py`
- `requirements.txt`
- `README.md`

#### Step 3: Deploy

- Click "Commit changes"
- Space will automatically restart

### Method 3: Hugging Face CLI Deployment

```bash
# Install Hugging Face CLI
pip install huggingface_hub

# Login
huggingface-cli login --token YOUR_TOKEN

# Deploy
huggingface-cli upload nellaivijay/research-assistant . --repo-type space
```

## GitHub Pages Deployment

### Method 1: Automatic Deployment (Recommended)

#### Step 1: Enable GitHub Pages

1. Go to repository Settings → Pages
2. Source: "GitHub Actions"
3. Save settings

#### Step 2: Verify Workflow

The `.github/workflows/docs-deploy.yml` workflow will automatically:
- Build documentation
- Deploy to GitHub Pages
- Update on every push to docs/

### Method 2: Manual Deployment

#### Step 1: Build Documentation

```bash
# Ensure docs are ready
ls docs/
# Should contain index.html
```

#### Step 2: Create gh-pages Branch

```bash
# Create orphan branch
git checkout --orphan gh-pages
git reset --hard
git commit --allow-empty -m "Initial commit"
git push origin gh-pages
git checkout main
```

#### Step 3: Deploy Documentation

```bash
# Copy docs to branch
git checkout gh-pages
git checkout main -- docs/
git add docs/
git commit -m "Update documentation"
git push origin gh-pages
git checkout main
```

## Manual Deployment

### Self-Hosted Deployment

#### Step 1: System Requirements

- Ubuntu 20.04+ or similar
- Python 3.10+
- 4GB RAM minimum
- 20GB disk space

#### Step 2: Install Dependencies

```bash
# Update system
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv /opt/research-assistant
source /opt/research-assistant/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Configure Service

```bash
# Create systemd service
sudo nano /etc/systemd/system/research-assistant.service
```

Add:
```ini
[Unit]
Description=Research Assistant
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/ramdov/projects/research-assistant
ExecStart=/opt/research-assistant/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Step 4: Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable research-assistant
sudo systemctl start research-assistant
```

### Docker Deployment

#### Step 1: Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Expose port
EXPOSE 7860

# Run application
CMD ["python", "app.py"]
```

#### Step 2: Build Image

```bash
docker build -t research-assistant .
```

#### Step 3: Run Container

```bash
docker run -d -p 7860:7860 --name research-assistant research-assistant
```

## CI/CD Deployment

### GitHub Actions Configuration

The project uses GitHub Actions for automated deployment:

#### CI/CD Pipeline (`.github/workflows/ci-cd.yml`)

**Triggers:**
- Push to `main` branch
- Pull requests to `main` branch

**Stages:**
1. Syntax check
2. Dependency installation
3. Hugging Face deployment

**Deployment Steps:**
```yaml
- name: Deploy to Hugging Face Spaces
  env:
    HF_TOKEN: ${{ secrets.HF_TOKEN }}
  run: |
    git remote remove hf || true
    git remote add hf https://nellaivijay:$HF_TOKEN@huggingface.co/spaces/nellaivijay/research-assistant.git
    git push hf main:main --force
```

### Manual CI/CD Trigger

```bash
# Using GitHub CLI
gh workflow run ci-cd.yml

# Using GitHub API
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/nellaivijay/research-assistant/actions/workflows/ci-cd.yml/dispatches
```

## Environment Configuration

### Production Environment Variables

**Hugging Face Spaces Secrets:**
1. Go to Space Settings → Variables
2. Add secrets:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `GOOGLE_API_KEY`

**GitHub Secrets:**
1. Go to repository Settings → Secrets → Actions
2. Add secret:
   - `HF_TOKEN` (for CI/CD deployment)

### Environment-Specific Configuration

**Development:**
```python
# Use local models, debug mode
DEBUG = True
LOG_LEVEL = "DEBUG"
```

**Production:**
```python
# Use production models, optimize for performance
DEBUG = False
LOG_LEVEL = "INFO"
CACHE_ENABLED = True
```

## Deployment Verification

### Hugging Face Spaces Verification

1. **Check Space Status**:
   - Go to https://huggingface.co/spaces/nellaivijay/research-assistant
   - Status should show "Running"

2. **Test Application**:
   - Click "App" tab
   - Verify all tabs are visible
   - Test basic functionality

3. **Check Logs**:
   - Click "Logs" tab
   - Verify no errors in startup logs

### GitHub Pages Verification

1. **Check Deployment Status**:
   - Go to repository Settings → Pages
   - Status should show "Active"

2. **Visit Site**:
   - Go to https://nellaivijay.github.io/research-assistant
   - Verify site loads correctly

3. **Check Workflow**:
   - Go to Actions tab
   - Verify docs-deploy workflow succeeded

### CI/CD Verification

1. **Check Workflow Runs**:
   - Go to https://github.com/nellaivijay/research-assistant/actions
   - Verify latest run shows green checkmark

2. **Check Deployment**:
   - Verify Hugging Face Space updated
   - Check deployment time

3. **Monitor Logs**:
   - Click on workflow run
   - Review each step's logs

## Rollback Procedures

### Hugging Face Spaces Rollback

#### Method 1: Git Rollback

```bash
# Rollback to previous commit
git log --oneline
git checkout <previous-commit-hash>
git push hf main --force
```

#### Method 2: Web Interface Rollback

1. Go to Space → Files
2. Click "History" on a file
3. Click "Rollback"
4. Space will restart with previous version

### GitHub Pages Rollback

#### Git Rollback

```bash
# Rollback documentation
git checkout gh-pages
git revert HEAD
git push origin gh-pages
git checkout main
```

### CI/CD Rollback

#### Disable CI/CD

```bash
# Remove workflow
rm .github/workflows/ci-cd.yml
git add .github/workflows/ci-cd.yml
git commit -m "Disable CI/CD"
git push github main
```

#### Manual Deployment

```bash
# Deploy manually while CI/CD is disabled
git push hf main
```

## Deployment Best Practices

### Pre-Deployment Checklist

- [ ] All tests pass locally
- [ ] No syntax errors
- [ ] Dependencies updated
- [ ] Configuration verified
- [ ] Documentation updated
- [ ] Backup created

### Deployment Strategy

**Blue-Green Deployment:**
- Deploy to test environment first
- Verify functionality
- Switch production to new version
- Keep old version for rollback

**Canary Deployment:**
- Deploy to subset of users
- Monitor for issues
- Gradually roll out to all users
- Quick rollback if issues arise

### Monitoring

**Key Metrics to Monitor:**
- Application uptime
- Response time
- Error rates
- Resource usage
- User feedback

### Security Considerations

**Production Security:**
- Use environment variables for secrets
- Enable HTTPS
- Regular security updates
- Monitor for vulnerabilities
- Rate limiting for API calls

---

**For more information, visit the [GitHub Repository](https://github.com/nellaivijay/research-assistant)**