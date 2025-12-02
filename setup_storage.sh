#!/bin/bash
# Supabase Storage Integration - Quick Setup Script
# Run this after configuring your .env file with Supabase credentials

echo "🚀 Setting up Supabase Storage Integration for PallettePartner"
echo "================================================================"

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not detected. Activating..."
    source venv/bin/activate || source venv/Scripts/activate
fi

# Install new dependencies
echo ""
echo "📦 Installing new packages..."
pip install django-storages==1.14.4 boto3==1.35.76 supabase==2.10.0 whitenoise==6.8.2

# Check if .env file exists
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  .env file not found!"
    echo "📄 Copying .env.example to .env..."
    cp .env.example .env
    echo "✅ Done! Please edit .env with your Supabase credentials."
    echo ""
    echo "Required variables:"
    echo "  - SECRET_KEY"
    echo "  - DATABASE_URL"
    echo "  - USE_SUPABASE_STORAGE=true (for production)"
    echo "  - SUPABASE_URL"
    echo "  - SUPABASE_STORAGE_BUCKET_NAME"
    echo "  - SUPABASE_ACCESS_KEY_ID"
    echo "  - SUPABASE_SECRET_ACCESS_KEY"
    echo ""
    exit 1
fi

# Check database connection
echo ""
echo "🗄️  Checking database connection..."
python manage.py check --database default

# Run migrations (if needed)
echo ""
echo "🔄 Running migrations..."
python manage.py migrate

# Test Supabase storage configuration
echo ""
echo "🧪 Testing Supabase Storage configuration..."
python -c "
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
"

# Collect static files (if using Supabase Storage)
USE_STORAGE=$(grep USE_SUPABASE_STORAGE .env | cut -d '=' -f2)
if [ "$USE_STORAGE" == "true" ]; then
    echo ""
    echo "📁 Collecting static files to Supabase Storage..."
    python manage.py collectstatic --no-input
fi

echo ""
echo "================================================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Review DEPLOYMENT.md for detailed instructions"
echo "  2. Create Supabase Storage bucket: 'pallettepartner-media'"
echo "  3. Configure bucket policies (see DEPLOYMENT.md)"
echo "  4. Test file uploads locally"
echo "  5. Deploy to Render or your hosting platform"
echo ""
echo "Run the server:"
echo "  python manage.py runserver"
echo "================================================================"
