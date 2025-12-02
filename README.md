# Project Title and Short Description
- PallettePartner is a web-based platform designed to connect traditional and digital artists for creative collaboration. The system enables users to create detailed profiles, post collaboration requests, and receive suggested matches based on shared artistic interests.

## Tech stack used
- Backend: Python 3.10+, Django 5.2.7
- Database: PostgreSQL (Supabase)
- Frontend: Django templates, Tailwind CSS (CDN), vanilla JavaScript modules
- Storage: Local file system (development), Supabase Storage (production)
- File Storage Backend: django-storages with boto3 (S3-compatible)
- Dev tooling: pip, virtualenv, manage.py

## Setup & run instructions

### Development Setup (Local)
1. Clone repository and open the project folder:
   ```bash
   git clone <repo-url>
   cd CSIT327-G1-PallettePartner
   ```

2. Create and activate virtual environment:
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. Apply migrations:
   ```bash
   python manage.py migrate
   ```

6. Run development server:
   ```bash
   python manage.py runserver
   ```

7. Open browser:
   - http://127.0.0.1:8000

### Production Deployment (Supabase Storage)

For deploying with Supabase Storage for user uploads and static files:

1. **Quick Setup** (Automated):
   - **Windows**: Run `.\setup_storage.ps1`
   - **macOS/Linux**: Run `./setup_storage.sh`

2. **Manual Setup**:
   - Follow the comprehensive guide in `DEPLOYMENT.md`
   - Configure Supabase Storage bucket
   - Set environment variables
   - Deploy to Render or your hosting platform

3. **Key Features**:
   - ✅ User uploads stored in Supabase Storage (avatars, artworks, chat images)
   - ✅ Static files (CSS, JS, icons) served from Supabase
   - ✅ Automatic file persistence across deployments
   - ✅ Scalable storage for production use

**Documentation**:
- `DEPLOYMENT.md` - Complete deployment guide
- `SUPABASE_STORAGE_IMPLEMENTATION.md` - Technical implementation details
- `.env.example` - Environment variable template

## The Team/Creators
- Michael C. Gelera - Project Owner - michael.gelera@cit.edu
- Christian James Gorre - Scrum Master - christianjames.gorre@cit.edu
- Daniel Luis P. Garcia - Business Analyst - danielluis.garcia@cit.edu
- Ma. Melessa V. Cabasag - Lead Developer - mamelessa.cabasag@cit.edu
- Van Andrae P. Bigtasin - Developer 1 - vanandrae.bigtasin@cit.edu
- Earl Ray T. Caaway - Developer 2 - earl.caaway@cit.edu 