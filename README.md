# Project Title and Short Description
- PallettePartner is a web-based platform designed to connect traditional and digital artists for creative collaboration. The system enables users to create detailed profiles, post collaboration requests, and receive suggested matches based on shared artistic interests.

## Tech stack used
- Backend: Python 3.10+, Django (Django REST or standard views where used)
- Database: SQLite (development), compatible with PostgreSQL for production
- Frontend: Django templates, Tailwind CSS (CDN or built assets), vanilla JavaScript modules
- Storage/Assets: Django static files (static/), media uploads via MEDIA settings
- Dev tooling: pip, virtualenv, manage.py, optional Node.js for Tailwind build

## Setup & run instructions
1. Clone repository and open the project folder:
   - Windows (PowerShell/CMD):
     - git clone <repo-url>
     - cd "d:\Codes\IM2\dev\PallettePartner-Collaboration-Finder-for-Artists"
2. Create and activate virtual environment:
   - python -m venv venv
   - venv\Scripts\activate
3. Install dependencies:
   - If requirements.txt exists:
     - pip install -r requirements.txt
   - Otherwise:
     - pip install Django
4. Configure environment (optional):
   - Copy example env or update config/settings.py for DB, SECRET_KEY, DEBUG
5. Apply migrations:
   - python manage.py migrate
6. (Optional) Create a superuser:
   - python manage.py createsuperuser
7. Run development server:
   - python manage.py runserver
8. Open browser:
   - http://127.0.0.1:8000

## The Team/Creators
- Michael C. Gelera - Project Owner - michael.gelera@cit.edu
- Christian James Gorre - Scrum Master - christianjames.gorre@cit.edu
- Daniel Luis P. Garcia - Business Analyst - danielluis.garcia@cit.edu
- Ma. Melessa V. Cabasag - Lead Developer - mamelessa.cabasag@cit.edu
- Van Andrae P. Bigtasin - Developer 1 - vanandrae.bigtasin@cit.edu
- Earl Ray T. Caaway - Developer 2 - earl.caaway@cit.edu 