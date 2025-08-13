# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Django Management
- `python manage.py runserver` - Start development server (requires PostgreSQL)
- `python manage.py migrate` - Apply database migrations
- `python manage.py makemigrations` - Create new migrations
- `python manage.py createsuperuser` - Create admin user
- `python manage.py collectstatic` - Collect static files
- `python manage.py test` - Run Django tests

### Docker Development
- `docker-compose up --build` - Build and start application with all services
- `docker-compose -f docker-compose.test.yml up --build` - Run test environment
- `docker-compose -f docker-compose.sandbox.yml up --build` - Run sandbox environment

## Architecture Overview

This is a Django web application for managing the Nebraska Statewide Plan for Community Well-Being. The project follows a modular architecture:

### Project Structure
- `statewideplanCWB/` - Main Django project settings and configuration
- `core/` - Primary application containing business logic, organized into submodules:
  - `plan_work/` - Core plan elements (Goals, Objectives, Strategies, Action Steps)
  - `plan_actors/` - Entities involved (Community Collaboratives, NCFF Teams, System Partners)
  - `standardization/` - Standardized choices and dropdowns
  - `alignment/` - External stakeholder alignment
  - `measurement/` - Performance measurement models
  - `relationships/` - Inter-entity relationships
- `users/` - Custom user authentication and management

### Key Models Hierarchy
- **Goal** → **Objective** → **Strategy** → **Action Steps/Commitments**
- **Plan Actors**: Community Collaboratives, NCFF Teams, System Partners
- **Action Steps**: CommunityActionStep, NCActionStep, SystemPartnerCommitment

### Database
- Uses PostgreSQL in all environments
- Environment-specific database configurations (development, test, sandbox, production)
- Database credentials managed through environment variables via python-decouple

### Authentication
- Custom user model (`users.AppUser`) extending AbstractBaseUser
- Users linked to Community Collaboratives, NCFF Teams, or System Partners
- Password reset middleware for new users

### Key Dependencies
- Django 4.2.14 with PostgreSQL (psycopg2)
- django-smart-selects for chained dropdowns
- django-widget-tweaks for form styling
- WhiteNoise for static file serving
- Gunicorn for production deployment

### Environment Configuration
The application supports multiple environments (development, test, sandbox, production) configured via `DJANGO_ENV` environment variable. Each environment has specific database, security, and domain settings.

### Permissions
Custom permissions system in `core/permissions.py` manages access control for different user types and their associated action steps.

### Admin Interface
Comprehensive Django admin interface with custom admin classes for all models, organized in separate admin modules within `core/admin/`.