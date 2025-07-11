# Deployment Guide - Cloudflare Pages

This guide will walk you through deploying your BookTranslator frontend to Cloudflare Pages.

## Prerequisites

- Cloudflare account
- GitHub/GitLab repository with your code
- Supabase project configured
- Translation API backend running

## Method 1: Git Integration (Recommended)

### 1. Push to Git Repository

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/astro-translation-frontend.git
git push -u origin main
```

### 2. Connect to Cloudflare Pages

1. Go to [Cloudflare Pages](https://pages.cloudflare.com/)
2. Click "Create a project"
3. Select "Connect to Git"
4. Choose your repository
5. Configure build settings:

#### Build Configuration
- **Framework preset**: Astro
- **Build command**: `npm run build`
- **Build output directory**: `dist`
- **Root directory**: `/` (unless your project is in a subdirectory)

#### Environment Variables
Add these in the "Environment variables" section:

```env
PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
PUBLIC_TRANSLATION_API_URL=https://your-api-domain.com
```

### 3. Deploy

Click "Save and Deploy". Cloudflare will:
- Clone your repository
- Install dependencies
- Build your project
- Deploy to a `.pages.dev` domain

## Method 2: Wrangler CLI

### 1. Install Wrangler

```bash
npm install -g wrangler
```

### 2. Login to Cloudflare

```bash
wrangler login
```

### 3. Build and Deploy

```bash
# Build the project
npm run build

# Deploy to Cloudflare Pages
wrangler pages deploy dist --project-name=astro-translation-frontend
```

## Post-Deployment Configuration

### 1. Custom Domain (Optional)

1. Go to your Pages project dashboard
2. Click "Custom domains"
3. Add your domain
4. Follow DNS configuration instructions

### 2. Environment Variables Management

Environment variables can be updated in the Pages dashboard:
1. Go to your project
2. Click "Settings" → "Environment variables"
3. Add/edit variables for Production and Preview

### 3. Build Configuration

Advanced build settings can be configured:
1. Go to "Settings" → "Builds & deployments"
2. Modify build commands, output directory, etc.

## Automatic Deployments

Once connected to Git, Cloudflare Pages will automatically:
- Deploy on every push to main branch
- Create preview deployments for pull requests
- Show deployment status in GitHub/GitLab

## Environment-Specific Configuration

### Production Environment Variables
```env
PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
PUBLIC_TRANSLATION_API_URL=https://your-production-api.com
```

### Preview Environment Variables
```env
PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
PUBLIC_TRANSLATION_API_URL=https://your-staging-api.com
```

## Troubleshooting

### Common Issues

1. **Build Fails with "Command not found"**
   - Ensure Node.js version is set to 18 or higher
   - Check build command is correct: `npm run build`

2. **Environment Variables Not Working**
   - Ensure variables are prefixed with `PUBLIC_`
   - Check variables are set in the correct environment (Production/Preview)
   - Restart deployment after adding variables

3. **API Calls Failing**
   - Verify API URL is correct and accessible
   - Check CORS settings on your backend
   - Ensure API is deployed and running

4. **Supabase Authentication Issues**
   - Verify Supabase URL and keys
   - Check that the site URL is added to Supabase allowed origins
   - Ensure email authentication is enabled

### Debug Steps

1. **Check Build Logs**
   - Go to your project dashboard
   - Click on a deployment
   - Review build and deployment logs

2. **Test Environment Variables**
   - Add `console.log` statements to verify variables are loaded
   - Check browser developer tools for values

3. **Verify API Connectivity**
   - Test API endpoints manually
   - Check network tab in browser dev tools
   - Verify CORS headers

## Performance Optimization

### Caching
Cloudflare Pages automatically provides:
- Global CDN distribution
- Automatic compression
- Static asset caching

### Additional Optimizations
- Images are automatically optimized
- CSS and JS are minified
- HTTP/2 and HTTP/3 support

## Security

### HTTPS
- Automatic HTTPS with Let's Encrypt certificates
- HTTP to HTTPS redirects
- HSTS headers

### Content Security Policy
Add CSP headers in `public/_headers`:

```
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
```

## Monitoring

### Analytics
Enable Cloudflare Web Analytics:
1. Go to your domain in Cloudflare
2. Click "Analytics & Logs" → "Web Analytics"
3. Enable analytics for your site

### Logs
Access deployment and function logs:
1. Go to Pages project dashboard
2. Click "Functions" → "Logs"
3. View real-time logs

## Rollback

If you need to rollback a deployment:
1. Go to project dashboard
2. Click "Deployments"
3. Find the previous working deployment
4. Click "Rollback to this deployment"

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    - name: Install dependencies
      run: npm ci
    - name: Build
      run: npm run build
    - name: Deploy to Cloudflare Pages
      uses: cloudflare/pages-action@v1
      with:
        apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
        accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
        projectName: astro-translation-frontend
        directory: dist
```

## Cost Considerations

Cloudflare Pages offers:
- **Free tier**: 500 builds/month, unlimited sites
- **Paid tier**: $20/month for unlimited builds
- **Bandwidth**: Unlimited on all plans
- **Storage**: 25GB included

## Support

For deployment issues:
- [Cloudflare Pages Documentation](https://developers.cloudflare.com/pages/)
- [Cloudflare Community](https://community.cloudflare.com/)
- [GitHub Issues](https://github.com/cloudflare/pages-action/issues) for Pages Action

For application issues:
- Check your project's GitHub issues
- Review browser console for errors
- Test API endpoints independently