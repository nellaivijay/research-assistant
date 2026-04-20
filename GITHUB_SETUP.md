# GitHub Setup Guide for Research Assistant

This guide will help you set up GitHub integration with automated CI/CD pipeline for the Research Assistant project.

## 🚀 Quick Setup

### 1. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `research-assistant` (or your preferred name)
3. Set as Public or Private (your preference)
4. Don't initialize with README (we already have one)
5. Click "Create repository"

### 2. Add GitHub Remote

```bash
cd /home/ramdov/projects/research-assistant
git remote add github https://github.com/nellaivijay/research-assistant.git
```

### 3. Configure GitHub Secrets

You need to add your Hugging Face token as a GitHub secret for automated deployment:

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `HF_TOKEN`
5. Value: Your Hugging Face access token
6. Click **Add secret**

**To get your Hugging Face token:**
- Go to https://huggingface.co/settings/tokens
- Create a new token with "Write" permissions
- Copy the token (starts with `hf_`)

### 4. Push to GitHub

```bash
# Push current code to GitHub
git push github main
```

### 5. Verify GitHub Actions

1. Go to your GitHub repository
2. Click on **Actions** tab
3. You should see the CI/CD pipeline running
4. The workflow will:
   - Run syntax checks
   - Install dependencies
   - Run basic tests
   - Deploy to Hugging Face (if on main branch)

## 📋 GitHub Actions Workflow

The CI/CD pipeline (`.github/workflows/ci-cd.yml`) includes:

### ✅ Testing Stage (runs on all branches)
- **Syntax Check**: Validates Python syntax
- **Dependency Installation**: Installs all requirements
- **Basic Tests**: Tests imports and model configuration
- **Security Check**: Scans for hardcoded credentials

### 🚀 Deployment Stage (runs only on main branch)
- **Automated Deployment**: Pushes to Hugging Face Spaces
- **Triggered**: Only after successful tests
- **Condition**: Only on push to main branch

## 🔧 Workflow Triggers

The GitHub Actions workflow runs on:
- **Push to main**: Full CI/CD + deployment
- **Push to develop**: CI/CD only (no deployment)
- **Pull requests to main**: CI/CD only (no deployment)

## 📊 Workflow Benefits

### ✅ Advantages
- **Automated Testing**: Catches errors before deployment
- **Continuous Integration**: Tests every change
- **Automated Deployment**: No manual deployment needed
- **Code Quality**: Ensures code standards
- **Security**: Scans for credentials
- **Backup**: GitHub serves as code backup

### 🔄 Development Workflow

1. **Make changes** locally
2. **Test locally** with `python -m py_compile app.py`
3. **Commit changes**: `git commit -am "Your message"`
4. **Push to GitHub**: `git push github main`
5. **GitHub Actions** automatically:
   - Runs tests
   - Deploys to Hugging Face if tests pass
6. **Monitor** in GitHub Actions tab

## 🐛 Troubleshooting

### GitHub Actions Failures

**If tests fail:**
1. Check the Actions tab for error details
2. Fix the issue locally
3. Push the fix
4. Actions will automatically retry

**If deployment fails:**
1. Verify `HF_TOKEN` secret is set correctly
2. Check token has "Write" permissions
3. Verify Hugging Face Space URL in workflow file

### Manual Deployment

If GitHub Actions fail, you can always deploy manually:

```bash
git push origin main
```

This pushes directly to Hugging Face (current setup).

## 📝 Best Practices

1. **Branch Protection**: Enable branch protection on main
2. **Pull Requests**: Use PRs for code review
3. **Test Locally**: Always test before pushing
4. **Monitor Actions**: Check Actions tab regularly
5. **Secret Security**: Never commit secrets or tokens

## 🔐 Security Notes

- **HF_TOKEN**: Stored as GitHub secret (never in code)
- **API Keys**: Use environment variables, never hardcode
- **Data Files**: `.gitignore` prevents committing data
- **Logs**: `.gitignore` prevents committing log files

## 🎯 Next Steps

After setup:
1. ✅ Push code to GitHub
2. ✅ Verify GitHub Actions run successfully
3. ✅ Check deployment to Hugging Face
4. ✅ Test the live application
5. ✅ Set up branch protection (optional)

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

---

**Your Research Assistant is now set up with professional-grade CI/CD pipeline!** 🎉