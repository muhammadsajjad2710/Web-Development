# GitHub App Setup for PostAI Ops Scanner

## Required Environment Variables

Add these to your environment (`.env` file or server configuration):

```bash
GITHUB_APP_ID=123456
GITHUB_APP_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here
```

## GitHub App Configuration

### 1. Create GitHub App

Go to GitHub Settings > Developer settings > GitHub Apps > New GitHub App

**Basic Information:**
- App Name: `PostAI Ops Security Scanner`
- Homepage URL: `https://your-domain.com/scan-github.php`
- Description: `Automated security vulnerability scanner for repositories`

### 2. Permissions Required

**Repository Permissions:**
- Contents: `Read` (to clone and read repository files)
- Metadata: `Read` (to access repository information)
- Pull requests: `Read` (optional, for PR scanning)

**Account Permissions:**
- Email addresses: `Read` (optional, for notifications)

### 3. Webhook Configuration

**Webhook URL:** `https://your-domain.com/scan-github.php`

**Events to Subscribe:**
- [x] Push
- [x] Pull request
- [x] Repository (for installation events)

**Webhook Secret:** Generate a secure random string and set as `GITHUB_WEBHOOK_SECRET`

### 4. Private Key Generation

After creating the app:
1. Scroll to "Private keys" section
2. Click "Generate a private key"
3. Download the `.pem` file
4. Convert to environment variable format:

```bash
# Convert PEM to single-line format
cat your-app-private-key.pem | tr '\n' ' ' | sed 's/ /\\n/g'
```

### 5. Installation

**For Organization/User Repositories:**
1. Go to your GitHub App settings
2. Click "Install App" in left sidebar
3. Choose organization/account
4. Select repositories to grant access
5. Complete installation

## Required Dependencies

Install via Composer:

```bash
composer require firebase/php-jwt
```

Add to `composer.json`:
```json
{
    "require": {
        "firebase/php-jwt": "^6.0"
    }
}
```

## Webhook Event Handling

The scanner responds to:

### Push Events
```json
{
    "repository": {
        "owner": {"login": "username"},
        "name": "repository-name"
    },
    "after": "commit-sha"
}
```

### Pull Request Events
```json
{
    "action": "opened|synchronize",
    "repository": {
        "owner": {"login": "username"}, 
        "name": "repository-name"
    },
    "pull_request": {
        "head": {"sha": "commit-sha"}
    }
}
```

## Security Features

1. **JWT Authentication**: App-level authentication with GitHub
2. **Installation Tokens**: Repository-scoped short-lived tokens
3. **Webhook Verification**: HMAC signature validation
4. **Temporary Storage**: Clone to temp directory, auto-cleanup
5. **Minimal Permissions**: Only requests necessary repository access

## API Usage

### Direct Scan Request
```bash
curl -X POST https://your-domain.com/scan-github.php \
  -H "Content-Type: application/json" \
  -d '{
    "action": "scan_github_app",
    "owner": "username",
    "repo": "repository-name", 
    "sha": "optional-commit-sha"
  }'
```

### Response Format
```json
{
    "success": true,
    "report": {
        "repo_name": "repository-name",
        "scan_timestamp": "2025-08-02T...",
        "total_issues_checked": 29,
        "issues_found": [...],
        "summary": {...}
    }
}
```

## Troubleshooting

### Common Issues

1. **"GitHub App not installed"**
   - Verify app is installed on target repository
   - Check repository owner/name spelling

2. **"Failed to get installation token"**
   - Verify `GITHUB_APP_ID` is correct
   - Check private key format in environment variable
   - Ensure app has required permissions

3. **"Invalid signature"**
   - Verify `GITHUB_WEBHOOK_SECRET` matches GitHub App configuration
   - Check webhook URL is accessible

4. **"Failed to clone repository"**
   - Verify installation token has Contents:Read permission
   - Check repository exists and is accessible
   - Ensure git is installed on server

### Debug Mode

Add debug logging by setting:
```bash
GITHUB_APP_DEBUG=true
```

This will log JWT tokens, API responses, and git commands for troubleshooting.