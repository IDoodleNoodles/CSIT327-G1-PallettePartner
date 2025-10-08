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
     - go to the repository folder
2. Create and activate virtual environment:
   - python -m venv venv
   - venv\Scripts\Activate.ps1
3. Install dependencies:
    - pip install Django
    - pip install psycopg2 dj-database-url python-dotenv
    - rename .env.preconfig to .env
4. Apply migrations:
   - python manage.py migrate
5. Run development server:
   - python manage.py runserver
6. Open browser:
   - http://127.0.0.1:8000

## The Team/Creators
- Michael C. Gelera - Project Owner - michael.gelera@cit.edu
- Christian James Gorre - Scrum Master - christianjames.gorre@cit.edu
- Daniel Luis P. Garcia - Business Analyst - danielluis.garcia@cit.edu
- Ma. Melessa V. Cabasag - Lead Developer - mamelessa.cabasag@cit.edu
- Van Andrae P. Bigtasin - Developer 1 - vanandrae.bigtasin@cit.edu
- Earl Ray T. Caaway - Developer 2 - earl.caaway@cit.edu 