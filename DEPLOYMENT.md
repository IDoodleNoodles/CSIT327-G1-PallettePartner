# PallettePartner Deployment Guide

## Overview
This guide covers deploying PallettePartner with Supabase Storage integration for user-uploaded files (avatars, artworks, chat images) and static files (CSS, JS, icons).

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Supabase Storage Setup](#supabase-storage-setup)
3. [Environment Configuration](#environment-configuration)
4. [Deploying to Render](#deploying-to-render)
5. [Static Files & Icons Fix](#static-files--icons-fix)
6. [Testing the Deployment](#testing-the-deployment)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts
- [Supabase Account](https://supabase.com) (for database + storage)
- [Render Account](https://render.com) or similar hosting platform
- Git repository (GitHub, GitLab, etc.)

### Local Development
- Python 3.10+
- PostgreSQL (via Supabase)
- Virtual environment activated

---

## Supabase Storage Setup

### Step 1: Create Supabase Storage Bucket

1. **Login to Supabase Dashboard**: https://app.supabase.com

2. **Navigate to Storage**:
   - Click on "Storage" in the left sidebar
   - Click "New Bucket"

3. **Create Bucket**:
   - **Name**: `pallettepartner-media`
   - **Public**: ✅ Enable (required for public access to images)
   - Click "Create bucket"

4. **Configure Bucket Policies** (Important for file access):
   - Click on the bucket name
   - Go to "Policies" tab
   - Add the following policies:

   **Policy 1: Public Read Access**
   ```sql
   CREATE POLICY "Public Read Access"
   ON storage.objects FOR SELECT
   USING (bucket_id = 'pallettepartner-media');
   ```

   **Policy 2: Authenticated Upload**
   ```sql
   CREATE POLICY "Authenticated Upload"
   ON storage.objects FOR INSERT
   WITH CHECK (bucket_id = 'pallettepartner-media' AND auth.role() = 'authenticated');
   ```

   **Policy 3: User Can Update Own Files**
   ```sql
   CREATE POLICY "Users Update Own Files"
   ON storage.objects FOR UPDATE
   USING (bucket_id = 'pallettepartner-media' AND auth.uid() = owner)
   WITH CHECK (bucket_id = 'pallettepartner-media');
   ```

   **Policy 4: User Can Delete Own Files**
   ```sql
   CREATE POLICY "Users Delete Own Files"
   ON storage.objects FOR DELETE
   USING (bucket_id = 'pallettepartner-media' AND auth.uid() = owner);
   ```

### Step 2: Generate S3 Access Keys

1. **Go to Settings > API**:
   - In Supabase Dashboard, click "Settings" (gear icon)
   - Select "API" from the left menu

2. **Find S3 Access Keys Section**:
   - Scroll down to "S3 Access Keys"
   - Click "Generate New Key"

3. **Save Credentials**:
   - Copy `Access Key ID`
   - Copy `Secret Access Key`
   - ⚠️ **Important**: Save these immediately - you won't see the secret again!

4. **Note Your Supabase URL**:
   - In "API Settings", copy your "Project URL"
   - Format: `https://xxxxx.supabase.co`

---

## Environment Configuration

### Step 1: Update Local .env File

Copy `.env.example` to `.env` and fill in values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Django Secret Key
SECRET_KEY=your-django-secret-key-here

# Supabase Database
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

# Enable Supabase Storage (set to 'true' for production)
USE_SUPABASE_STORAGE=true

# Supabase Storage Configuration
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_STORAGE_BUCKET_NAME=pallettepartner-media
SUPABASE_ACCESS_KEY_ID=your-access-key-id-from-step-2
SUPABASE_SECRET_ACCESS_KEY=your-secret-access-key-from-step-2
SUPABASE_REGION=us-east-1
```

### Step 2: Generate Django Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output to `SECRET_KEY` in `.env`

---

## Deploying to Render

### Step 1: Create New Web Service

1. **Login to Render**: https://dashboard.render.com

2. **New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your Git repository
   - Select the repository

3. **Configure Service**:
   - **Name**: `pallettepartner`
   - **Region**: Choose closest to your users
   - **Branch**: `main` or `feature/missing-features`
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
     ```
   - **Start Command**:
     ```bash
     gunicorn config.wsgi:application
     ```

### Step 2: Add Environment Variables

In Render Dashboard, go to "Environment" and add:

```
SECRET_KEY=<your-django-secret-key>
DATABASE_URL=<your-supabase-postgres-url>
USE_SUPABASE_STORAGE=true
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_STORAGE_BUCKET_NAME=pallettepartner-media
SUPABASE_ACCESS_KEY_ID=<your-access-key-id>
SUPABASE_SECRET_ACCESS_KEY=<your-secret-access-key>
SUPABASE_REGION=us-east-1
PYTHON_VERSION=3.10.0
```

### Step 3: Deploy

1. Click "Create Web Service"
2. Wait for build to complete (5-10 minutes)
3. Check logs for any errors

---

## Static Files & Icons Fix

### Problem: Missing Icons After Deployment

When deploying, icons and static files may not load because they need to be collected and uploaded to Supabase Storage.

### Solution: Collect Static Files to Supabase

#### Option 1: Automatic (via Build Command)

The build command includes `python manage.py collectstatic --no-input`, which will:
- Collect all static files from `static/` directories
- Upload them to Supabase Storage bucket under `static/` path
- Make them accessible via: `https://xxxxx.supabase.co/storage/v1/object/public/pallettepartner-media/static/`

#### Option 2: Manual Collection (if needed)

If icons are still missing:

1. **SSH into Render** (or run locally with production settings):
   ```bash
   # Set environment variable
   export USE_SUPABASE_STORAGE=true
   
   # Collect static files
   python manage.py collectstatic --no-input
   ```

2. **Verify Upload**:
   - Go to Supabase Dashboard > Storage > `pallettepartner-media`
   - Check for `static/` folder
   - Verify `static/icon/` contains all icon files

3. **Check File Permissions**:
   - Ensure bucket is set to "Public"
   - Verify policies allow public read access

### Verifying Icon URLs

Icons should be accessible at:
```
https://[PROJECT-REF].supabase.co/storage/v1/object/public/pallettepartner-media/static/icon/dashboard.png
https://[PROJECT-REF].supabase.co/storage/v1/object/public/pallettepartner-media/static/icon/profile_icon.png
```

Test by opening these URLs in a browser.

---

## Testing the Deployment

### 1. Check Static Files

Visit your deployed site and open browser DevTools (F12):
- **Console Tab**: Check for 404 errors on static files
- **Network Tab**: Filter by "CSS" and "JS" - all should load successfully
- **Images**: Icons should display correctly in navigation

### 2. Test File Uploads

#### Upload Avatar:
1. Login to your deployed site
2. Go to Profile → Edit Profile
3. Upload a new avatar image
4. Check Supabase Storage:
   - Go to Dashboard > Storage > `pallettepartner-media` > `media/avatars/`
   - Your uploaded image should appear

#### Upload Artwork:
1. Go to Dashboard
2. Click "Upload Artwork"
3. Select an image and submit
4. Check Supabase Storage:
   - Navigate to `media/artworks/`
   - Uploaded artwork should appear

#### Send Image in Chat:
1. Start a collaboration
2. Upload an image in chat
3. Check Supabase Storage:
   - Navigate to `media/chat_images/`
   - Chat image should appear

### 3. Verify Image Display

- Profile avatars should display correctly
- Artwork thumbnails should load on dashboard
- Chat images should appear in messages
- Default avatar should work for new users

---

## File Structure in Supabase Storage

After deployment, your bucket structure should look like:

```
pallettepartner-media/
├── static/
│   ├── css/
│   │   ├── loading.css
│   │   └── pallate.css
│   ├── js/
│   │   ├── animations.js
│   │   ├── cards.js
│   │   ├── chat.js
│   │   └── ... (all JS files)
│   └── icon/
│       ├── dashboard.png
│       ├── profile_icon.png
│       ├── notification_icon.png
│       └── ... (all icon files)
└── media/
    ├── avatars/
    │   ├── default.png
    │   └── user_uploads...
    ├── artworks/
    │   └── user_uploads...
    └── chat_images/
        └── user_uploads...
```

---

## Troubleshooting

### Issue: Icons Not Loading (404 Errors)

**Symptoms**: Browser console shows 404 errors for icon files

**Solutions**:

1. **Check STATIC_URL in settings.py**:
   ```python
   # Should be set when USE_SUPABASE_STORAGE=true
   STATIC_URL = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET_NAME}/static/"
   ```

2. **Re-run collectstatic**:
   ```bash
   python manage.py collectstatic --no-input --clear
   ```

3. **Verify bucket is public**:
   - Supabase Dashboard > Storage > Click bucket name
   - Check "Public bucket" toggle is ON

4. **Check storage policies**:
   - Ensure "Public Read Access" policy exists
   - Test by opening icon URL directly in browser

### Issue: Uploaded Files Not Appearing

**Symptoms**: Files upload successfully but don't display

**Solutions**:

1. **Check AWS credentials**:
   ```bash
   # Verify environment variables are set
   echo $SUPABASE_ACCESS_KEY_ID
   echo $SUPABASE_SECRET_ACCESS_KEY
   ```

2. **Verify bucket name**:
   - Should match exactly: `pallettepartner-media`
   - Check in Supabase Dashboard > Storage

3. **Check file permissions**:
   - Files should be readable by public
   - Verify policies allow authenticated uploads

4. **Inspect upload errors**:
   ```python
   # Add to settings.py for debugging
   AWS_S3_VERIFY = True
   AWS_S3_VERBOSE = True
   ```

### Issue: "Access Denied" Errors

**Symptoms**: S3 Access Denied errors in logs

**Solutions**:

1. **Regenerate S3 keys**:
   - Supabase Dashboard > Settings > API
   - Generate new S3 Access Keys
   - Update environment variables

2. **Check bucket policies**:
   - Ensure INSERT policy allows authenticated users
   - Verify UPDATE/DELETE policies for file owners

3. **Verify endpoint URL**:
   ```python
   AWS_S3_ENDPOINT_URL = f"{SUPABASE_URL}/storage/v1/s3"
   ```

### Issue: Slow File Uploads

**Symptoms**: File uploads take a long time

**Solutions**:

1. **Use closer Supabase region**:
   - Choose region closest to your users
   - Update `SUPABASE_REGION` if needed

2. **Enable caching**:
   ```python
   AWS_S3_OBJECT_PARAMETERS = {
       'CacheControl': 'max-age=86400',  # 1 day cache
   }
   ```

3. **Compress images before upload**:
   - Consider using Pillow to resize/compress
   - Add image optimization in form validation

### Issue: CORS Errors

**Symptoms**: Browser shows CORS policy errors

**Solutions**:

1. **Configure CORS in Supabase**:
   - Storage > Bucket Settings > CORS
   - Add your domain to allowed origins

2. **Check ALLOWED_HOSTS**:
   ```python
   ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com', 'your-domain.com']
   ```

3. **Update CSRF_TRUSTED_ORIGINS**:
   ```python
   CSRF_TRUSTED_ORIGINS = [
       'https://your-app.onrender.com',
       'https://your-domain.com'
   ]
   ```

---

## Development vs Production

### Development (Local)
- Set `USE_SUPABASE_STORAGE=false` in `.env`
- Files stored locally in `media/` folder
- Faster for development/testing
- No internet required for file access

### Production (Deployed)
- Set `USE_SUPABASE_STORAGE=true` in environment variables
- All files stored in Supabase Storage
- Accessible from anywhere
- Better scalability and reliability

---

## Cost Considerations

### Supabase Storage Pricing (as of 2024)

**Free Tier**:
- 1 GB storage
- 2 GB bandwidth/month
- Sufficient for small projects

**Pro Tier** ($25/month):
- 100 GB storage
- 200 GB bandwidth/month
- Better for production apps

**Pay-as-you-go**:
- $0.021/GB/month for storage
- $0.09/GB for bandwidth

### Tips to Reduce Costs:
1. Compress images before upload
2. Set reasonable file size limits
3. Implement file cleanup for deleted users
4. Use CDN caching (CloudFlare, etc.)

---

## Security Best Practices

1. **Never commit `.env` file**:
   - Add to `.gitignore`
   - Use environment variables in production

2. **Rotate S3 keys regularly**:
   - Generate new keys every 90 days
   - Update in Render dashboard

3. **Validate file uploads**:
   - Check file types (only images)
   - Limit file sizes (max 10MB)
   - Scan for malware if possible

4. **Use HTTPS only**:
   - Enforce in production settings
   - Set `SECURE_SSL_REDIRECT = True`

5. **Monitor storage usage**:
   - Check Supabase Dashboard regularly
   - Set up alerts for quota limits

---

## Additional Resources

- [Django-Storages Documentation](https://django-storages.readthedocs.io/)
- [Supabase Storage Guide](https://supabase.com/docs/guides/storage)
- [Render Deployment Docs](https://render.com/docs/deploy-django)
- [Django Static Files Guide](https://docs.djangoproject.com/en/stable/howto/static-files/deployment/)

---

## Quick Reference: Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Check deployment settings
python manage.py check --deploy
```

---

## Support

If you encounter issues:
1. Check the logs in Render Dashboard
2. Review Supabase Storage logs
3. Test locally with `USE_SUPABASE_STORAGE=true`
4. Verify all environment variables are set correctly
5. Check browser DevTools for network errors

---

## Summary

✅ **Supabase Storage** handles all user uploads (avatars, artworks, chat images)  
✅ **Static files** (CSS, JS, icons) uploaded via `collectstatic`  
✅ **Icons fixed** by collecting static files to Supabase  
✅ **Environment-based** configuration (local vs production)  
✅ **Secure** with proper bucket policies and access keys  
✅ **Scalable** for growing user base and file storage needs  

Your PallettePartner app is now ready for production deployment with proper file storage! 🚀
