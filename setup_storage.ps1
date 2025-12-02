# Supabase Storage Integration - Quick Setup Script (PowerShell)
# Run this after configuring your .env file with Supabase credentials

Write-Host "🚀 Setting up Supabase Storage Integration for PallettePartner" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not detected. Activating..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
}

# Install new dependencies
Write-Host ""
Write-Host "📦 Installing new packages..." -ForegroundColor Green
pip install django-storages==1.14.4 boto3==1.35.76 supabase==2.10.0 whitenoise==6.8.2

# Check if .env file exists
if (-not (Test-Path .env)) {
    Write-Host ""
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "📄 Copying .env.example to .env..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ Done! Please edit .env with your Supabase credentials." -ForegroundColor Green
    Write-Host ""
    Write-Host "Required variables:" -ForegroundColor Cyan
    Write-Host "  - SECRET_KEY"
    Write-Host "  - DATABASE_URL"
    Write-Host "  - USE_SUPABASE_STORAGE=true (for production)"
    Write-Host "  - SUPABASE_URL"
    Write-Host "  - SUPABASE_STORAGE_BUCKET_NAME"
    Write-Host "  - SUPABASE_ACCESS_KEY_ID"
    Write-Host "  - SUPABASE_SECRET_ACCESS_KEY"
    Write-Host ""
    exit 1
}

# Check database connection
Write-Host ""
Write-Host "🗄️  Checking database connection..." -ForegroundColor Green
python manage.py check --database default

# Run migrations (if needed)
Write-Host ""
Write-Host "🔄 Running migrations..." -ForegroundColor Green
python manage.py migrate

# Test Supabase storage configuration
Write-Host ""
Write-Host "🧪 Testing Supabase Storage configuration..." -ForegroundColor Green
python -c @"
import os
from dotenv import load_dotenv
load_dotenv()

use_storage = os.getenv('USE_SUPABASE_STORAGE', 'False').lower() == 'true'
if use_storage:
    supabase_url = os.getenv('SUPABASE_URL')
    bucket = os.getenv('SUPABASE_STORAGE_BUCKET_NAME')
    access_key = os.getenv('SUPABASE_ACCESS_KEY_ID')
    
    if not all([supabase_url, bucket, access_key]):
        print('❌ Missing Supabase Storage credentials!')
        print('   Please check your .env file.')
        exit(1)
    else:
        print('✅ Supabase Storage configuration found!')
        print(f'   URL: {supabase_url}')
        print(f'   Bucket: {bucket}')
else:
    print('ℹ️  Supabase Storage disabled (using local file system)')
"@

# Collect static files (if using Supabase Storage)
$envContent = Get-Content .env
$useStorage = ($envContent | Select-String "USE_SUPABASE_STORAGE=(.+)").Matches.Groups[1].Value

if ($useStorage -eq "true") {
    Write-Host ""
    Write-Host "📁 Collecting static files to Supabase Storage..." -ForegroundColor Green
    python manage.py collectstatic --no-input
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review DEPLOYMENT.md for detailed instructions"
Write-Host "  2. Create Supabase Storage bucket: 'pallettepartner-media'"
Write-Host "  3. Configure bucket policies (see DEPLOYMENT.md)"
Write-Host "  4. Test file uploads locally"
Write-Host "  5. Deploy to Render or your hosting platform"
Write-Host ""
Write-Host "Run the server:" -ForegroundColor Cyan
Write-Host "  python manage.py runserver" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
