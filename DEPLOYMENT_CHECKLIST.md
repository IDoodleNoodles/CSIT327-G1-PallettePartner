# Supabase Storage Setup Checklist

Use this checklist to ensure proper setup of Supabase Storage for PallettePartner.

---

## 📋 Pre-Deployment Checklist

### Local Development Setup
- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file exists with `USE_SUPABASE_STORAGE=false`
- [ ] Database migrations applied: `python manage.py migrate`
- [ ] Development server runs successfully: `python manage.py runserver`
- [ ] Can upload avatar locally (file saved to `media/avatars/`)
- [ ] Can upload artwork locally (file saved to `media/artworks/`)
- [ ] Icons display correctly in navigation

---

## 🗄️ Supabase Configuration Checklist

### 1. Supabase Project Setup
- [ ] Supabase account created
- [ ] Supabase project created
- [ ] PostgreSQL database configured
- [ ] Database URL added to `.env`

### 2. Storage Bucket Creation
- [ ] Navigate to Supabase Dashboard → Storage
- [ ] Click "New Bucket"
- [ ] Bucket name: `pallettepartner-media`
- [ ] Public access: ✅ **ENABLED** (very important!)
- [ ] Bucket created successfully

### 3. Bucket Policies Configuration
- [ ] Navigate to bucket → Policies tab
- [ ] **Policy 1: Public Read Access** created
  ```sql
  CREATE POLICY "Public Read Access"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'pallettepartner-media');
  ```
- [ ] **Policy 2: Authenticated Upload** created
  ```sql
  CREATE POLICY "Authenticated Upload"
  ON storage.objects FOR INSERT
  WITH CHECK (bucket_id = 'pallettepartner-media' AND auth.role() = 'authenticated');
  ```
- [ ] **Policy 3: Users Update Own Files** created
  ```sql
  CREATE POLICY "Users Update Own Files"
  ON storage.objects FOR UPDATE
  USING (bucket_id = 'pallettepartner-media' AND auth.uid() = owner)
  WITH CHECK (bucket_id = 'pallettepartner-media');
  ```
- [ ] **Policy 4: Users Delete Own Files** created
  ```sql
  CREATE POLICY "Users Delete Own Files"
  ON storage.objects FOR DELETE
  USING (bucket_id = 'pallettepartner-media' AND auth.uid() = owner);
  ```

### 4. S3 Access Keys Generation
- [ ] Navigate to Settings → API
- [ ] Scroll to "S3 Access Keys" section
- [ ] Click "Generate New Key"
- [ ] **Access Key ID** copied and saved securely
- [ ] **Secret Access Key** copied and saved securely
- [ ] ⚠️ **WARNING**: Secret key won't be shown again!

### 5. Environment Variables Configuration
- [ ] Supabase Project URL copied from Settings → API
- [ ] Update `.env` file with all Supabase credentials:
  ```env
  USE_SUPABASE_STORAGE=true
  SUPABASE_URL=https://xxxxx.supabase.co
  SUPABASE_STORAGE_BUCKET_NAME=pallettepartner-media
  SUPABASE_ACCESS_KEY_ID=your-access-key-id
  SUPABASE_SECRET_ACCESS_KEY=your-secret-access-key
  SUPABASE_REGION=us-east-1
  ```

---

## 🧪 Local Testing with Supabase Checklist

### Test with Supabase Storage Locally
- [ ] Set `USE_SUPABASE_STORAGE=true` in `.env`
- [ ] Restart Django server
- [ ] Server starts without errors
- [ ] Check console for: "✅ Using Supabase Storage for media and static files"

### Test File Uploads
- [ ] **Avatar Upload**:
  - [ ] Login to application
  - [ ] Go to Profile → Edit Profile
  - [ ] Upload new avatar image
  - [ ] Avatar displays correctly
  - [ ] Check Supabase Dashboard → Storage → Bucket
  - [ ] File appears in `media/avatars/` folder
  
- [ ] **Artwork Upload**:
  - [ ] Go to Dashboard
  - [ ] Click "Upload Artwork"
  - [ ] Select image and upload
  - [ ] Artwork appears on dashboard
  - [ ] Check Supabase Storage
  - [ ] File appears in `media/artworks/` folder
  
- [ ] **Chat Image Upload**:
  - [ ] Start a collaboration
  - [ ] Send message with image
  - [ ] Image displays in chat
  - [ ] Check Supabase Storage
  - [ ] File appears in `media/chat_images/` folder

### Test Static Files
- [ ] Run: `python manage.py collectstatic --no-input`
- [ ] Check Supabase Storage bucket
- [ ] `static/` folder exists in bucket
- [ ] `static/css/` contains CSS files
- [ ] `static/js/` contains JS files
- [ ] `static/icon/` contains all 15 icon files

---

## 🚀 Render Deployment Checklist

### 1. Render Web Service Creation
- [ ] Login to Render Dashboard
- [ ] Click "New +" → "Web Service"
- [ ] Connect Git repository
- [ ] Select repository: `CSIT327-G1-PallettePartner`
- [ ] Select branch: `main` or `feature/missing-features`

### 2. Service Configuration
- [ ] **Name**: `pallettepartner` (or your choice)
- [ ] **Region**: Choose closest to users
- [ ] **Runtime**: `Python 3`
- [ ] **Build Command**:
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
  ```
- [ ] **Start Command**:
  ```bash
  gunicorn config.wsgi:application
  ```
- [ ] **Instance Type**: Free or Starter (your choice)

### 3. Environment Variables (CRITICAL!)
Add these in Render Dashboard → Environment:

- [ ] `SECRET_KEY` = `<your-django-secret-key>`
- [ ] `DATABASE_URL` = `<your-supabase-postgres-url>`
- [ ] `USE_SUPABASE_STORAGE` = `true`
- [ ] `SUPABASE_URL` = `https://xxxxx.supabase.co`
- [ ] `SUPABASE_STORAGE_BUCKET_NAME` = `pallettepartner-media`
- [ ] `SUPABASE_ACCESS_KEY_ID` = `<your-access-key-id>`
- [ ] `SUPABASE_SECRET_ACCESS_KEY` = `<your-secret-access-key>`
- [ ] `SUPABASE_REGION` = `us-east-1`
- [ ] `PYTHON_VERSION` = `3.10.0` (optional)

### 4. Deploy
- [ ] Click "Create Web Service"
- [ ] Wait for build to complete (5-10 minutes)
- [ ] Check build logs for errors
- [ ] Deployment successful (no errors)

---

## ✅ Post-Deployment Verification Checklist

### 1. Application Health Check
- [ ] Deployed site loads successfully
- [ ] No 500/502 errors
- [ ] Can access login page
- [ ] Can register new account
- [ ] Can login with account

### 2. Static Files Verification
- [ ] Open browser DevTools (F12) → Console
- [ ] No 404 errors for CSS files
- [ ] No 404 errors for JS files
- [ ] No 404 errors for icon files
- [ ] Navigation icons display correctly
- [ ] Dashboard icon displays
- [ ] Profile icon displays

### 3. Icon URLs Verification
Test these URLs directly in browser (replace xxxxx with your project ref):
- [ ] `https://xxxxx.supabase.co/storage/v1/object/public/pallettepartner-media/static/icon/dashboard.png`
- [ ] `https://xxxxx.supabase.co/storage/v1/object/public/pallettepartner-media/static/icon/profile_icon.png`
- [ ] `https://xxxxx.supabase.co/storage/v1/object/public/pallettepartner-media/static/icon/notification_icon.png`
- [ ] All icons load successfully

### 4. File Upload Testing (Production)
- [ ] **Avatar Upload**:
  - [ ] Login to deployed site
  - [ ] Go to Profile → Edit Profile
  - [ ] Upload avatar
  - [ ] Avatar displays immediately
  - [ ] Check Supabase Storage
  - [ ] File appears in bucket
  
- [ ] **Artwork Upload**:
  - [ ] Upload artwork from dashboard
  - [ ] Artwork displays on timeline
  - [ ] Check Supabase Storage
  - [ ] File appears in `media/artworks/`
  
- [ ] **Chat Image Upload**:
  - [ ] Create collaboration
  - [ ] Upload image in chat
  - [ ] Image displays in messages
  - [ ] Check Supabase Storage
  - [ ] File appears in `media/chat_images/`

### 5. Supabase Storage Verification
- [ ] Login to Supabase Dashboard
- [ ] Navigate to Storage → `pallettepartner-media`
- [ ] Folder structure exists:
  ```
  pallettepartner-media/
  ├── media/
  │   ├── avatars/
  │   ├── artworks/
  │   └── chat_images/
  └── static/
      ├── css/
      ├── js/
      └── icon/
  ```
- [ ] Static files collected (CSS, JS, icons)
- [ ] User uploads appear in correct folders
- [ ] All files publicly accessible

### 6. Performance Check
- [ ] Page load time < 3 seconds
- [ ] Images load quickly
- [ ] No broken images
- [ ] No missing icons
- [ ] Console has no errors

---

## 🔧 Troubleshooting Checklist

### If Icons Not Loading (404 Errors)

- [ ] Check `USE_SUPABASE_STORAGE=true` is set
- [ ] Check `STATIC_URL` in deployed logs
- [ ] Re-run `collectstatic`:
  ```bash
  python manage.py collectstatic --no-input --clear
  ```
- [ ] Verify bucket is public
- [ ] Check bucket policies allow public read
- [ ] Test icon URL directly in browser
- [ ] Check Render build logs for collectstatic errors

### If File Uploads Fail

- [ ] Verify S3 access keys are correct
- [ ] Check environment variables in Render
- [ ] Regenerate S3 keys if needed
- [ ] Verify bucket name matches exactly
- [ ] Check bucket policies allow insert
- [ ] Review Render application logs
- [ ] Test with smaller file size (< 1MB)

### If "Access Denied" Errors

- [ ] Regenerate S3 Access Keys
- [ ] Update `SUPABASE_ACCESS_KEY_ID` in Render
- [ ] Update `SUPABASE_SECRET_ACCESS_KEY` in Render
- [ ] Restart Render service
- [ ] Check bucket policies are correct
- [ ] Verify `AWS_S3_ENDPOINT_URL` is correct

### If Static Files Not Collected

- [ ] Check build command includes `collectstatic`
- [ ] Verify `STATICFILES_STORAGE` is set correctly
- [ ] Check `SUPABASE_URL` environment variable
- [ ] Review Render build logs for errors
- [ ] Manually run collectstatic locally with `USE_SUPABASE_STORAGE=true`
- [ ] Check Supabase Storage for `static/` folder

---

## 📊 Monitoring Checklist

### Regular Maintenance
- [ ] Monitor Supabase storage usage (Dashboard → Settings → Usage)
- [ ] Check for orphaned files (deleted users' uploads)
- [ ] Review bandwidth usage monthly
- [ ] Monitor application logs in Render
- [ ] Check for security vulnerabilities
- [ ] Update dependencies regularly

### Storage Optimization
- [ ] Implement file size limits (10MB recommended)
- [ ] Compress images before upload (optional)
- [ ] Delete unused files periodically
- [ ] Monitor free tier limits (1GB storage, 2GB bandwidth)
- [ ] Consider upgrading if limits reached

---

## 📚 Documentation Reference

### Essential Documents
- [ ] Read `DEPLOYMENT.md` (comprehensive guide)
- [ ] Review `SUPABASE_STORAGE_IMPLEMENTATION.md` (technical details)
- [ ] Check `STORAGE_ARCHITECTURE.md` (visual diagrams)
- [ ] Reference `.env.example` (configuration template)

### Automation Scripts
- [ ] Review `setup_storage.ps1` (Windows setup)
- [ ] Review `setup_storage.sh` (Unix/Mac setup)

---

## ✨ Success Criteria

Your deployment is successful when:

✅ All checkboxes in this document are completed  
✅ Application loads without errors  
✅ All icons display correctly  
✅ Users can upload avatars  
✅ Users can upload artworks  
✅ Chat images work properly  
✅ Files persist after redeployment  
✅ Supabase Storage shows all uploaded files  
✅ No 404 errors in browser console  
✅ Page loads within 3 seconds  

---

## 🎯 Quick Command Reference

```bash
# Local development
python manage.py runserver

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate

# Check Django configuration
python manage.py check

# Check deployment readiness
python manage.py check --deploy

# Create superuser
python manage.py createsuperuser
```

---

## 📞 Support Resources

- **Django-Storages**: https://django-storages.readthedocs.io/
- **Supabase Storage**: https://supabase.com/docs/guides/storage
- **Render Deployment**: https://render.com/docs/deploy-django
- **Project Documentation**: See `DEPLOYMENT.md`

---

## ⏱️ Estimated Time

- **Supabase Setup**: 15-20 minutes
- **Local Testing**: 10-15 minutes
- **Render Deployment**: 10-15 minutes
- **Verification**: 10-15 minutes
- **Total**: ~45-65 minutes

---

## 🎉 Completion

Once all items are checked:

🎊 **Congratulations!** Your PallettePartner application is successfully deployed with Supabase Storage integration!

Next steps:
1. Share deployed URL with team
2. Test all features thoroughly
3. Monitor storage usage
4. Plan for scaling if needed
5. Implement additional features

---

**Last Updated**: December 2, 2025  
**Version**: 1.0  
**Status**: Production Ready ✅
