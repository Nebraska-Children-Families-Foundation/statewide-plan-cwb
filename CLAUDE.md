# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Core Development Philosophy

### KISS (Keep It Simple, Stupid)
Simplicity should be a key goal in design. Choose straightforward solutions over complex ones whenever possible. Simple solutions are easier to understand, maintain, and debug.

### YAGNI (You Aren't Gonna Need It)
Avoid building functionality on speculation. Implement features only when they are needed, not when you anticipate they might be useful in the future.

### Design Principles

#### Separation of Concerns
- **Modular Architecture**: Core application organized into focused submodules (`plan_work/`, `plan_actors/`, `standardization/`, `alignment/`, `measurement/`, `relationships/`)
- **Single Responsibility**: Each model and module handles a specific domain concept
- **Clear Boundaries**: Business logic separated from presentation (templates) and data access (models)

#### Domain-Driven Design
- **Hierarchical Relationships**: Clear Goal → Objective → Strategy → Action Steps hierarchy reflecting business domain
- **Ubiquitous Language**: Model names directly match business terminology (CommunityActionStep, SystemPartnerCommitment)
- **Aggregate Roots**: Primary entities (Goal, Strategy) serve as entry points to related data

#### Configuration Over Convention
- **Environment-Specific Settings**: Multi-environment support (development, test, sandbox, production) via environment variables
- **Centralized Configuration**: Settings managed through python-decouple for environment flexibility
- **Database Flexibility**: PostgreSQL across all environments with configurable connection parameters

#### Security by Design
- **Custom Authentication**: Purpose-built user model (`AppUser`) with role-based access control
- **Permission-Based Access**: Granular permissions system for action step editing based on user type and ownership
- **Secure Defaults**: CSRF protection, secure cookies, and environment-specific security settings

#### Data Integrity and Consistency
- **UUID Primary Keys**: Globally unique identifiers for all entities prevent ID conflicts
- **Automatic Number Generation**: Consistent numbering schemes (STRG-XXXX, C-ACT-XXXX, NC-ACT-XXXX) with automatic increment logic
- **Cascading Relationships**: Proper foreign key constraints with SET_NULL for optional relationships
- **Chained Dependencies**: Smart selects ensure data consistency in hierarchical relationships

#### Administrative Excellence
- **Comprehensive Admin Interface**: Custom admin classes for all models with organized imports
- **Descriptive Metadata**: Verbose names, help text, and proper ordering for enhanced usability
- **Audit Trail**: Creator tracking for action steps and commitments

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

## Project Purpose

The Statewide Plan for Community Well-Being Portal is a web application that has three main functions. First, it helps **Plan Actors** in carrying out the work of the Statewide Plan record their **Action Steps** or **Commitments**. Second, it provides the public with information about the Statewide Plan for Community Well-Being and allows them to see efforts happening at the community level. Finally, it is a resource that allows for peer-learning and continuous improvement through the sharing of lessons learned as Action Steps are worked on and completed.

### Plan Work
The Statewide Plan for Community Well-Being is a hierarchal plan consisting of 4 **Goals**. Each Goal has multiple **Objectives**. Each Objective has multiple **Strategies**. Strategies will have various **Action Steps** and **Commitments**.

Goals, Objectives, and Strategies were determined through a consultative process and do not change. Action Steps and Commitments are determined by Plan Actors and are regularly updated.

#### Recording Activities
- **Action Steps** are created and updated by **Community Collaboratives** and **NCFF Teams**.
- **Commitments** are created and maintained by **System Partners**.

##### Community Collaborative Action Steps
- Action Steps should be visible to logged in users only. Non-logged in users should not be able to see Action Step information.
- When an Action Step is created, the Action Step should be associated with the Community Collaborative *and* the user who has created it.
- Only members of a Community Collaborative should be able to edit Action Steps related to that Community Collaborative.
- Users with the role `Staff Member` or `NCFF Team Member` should be able to edit all Action Steps.
- If a Community Collaborative User is deleted, the Action Steps associated with them should be reassigned to another user.

##### Nebraska Children Action Steps
- Action Steps should be visible to logged in users only. Non-logged in users should not be able to see Action Step information.
- When an Action Step is created, the Action Step should be associated with the "NCFF Initiative / Team / Priority Area" *and* the user who has created it.
- Only members of the "NCFF Initiative / Team / Priority Area" *and* should be able to edit Nebraska Children Action Steps.
- Users with the role `Superuser` should be able to edit all Action Steps.
- If a NCFF Team Member user is deleted, the Action Steps associated with them should be reassigned to another user.

##### System Partner Commitments
- Commitments should be visible to logged in users only. Non-logged in user should not be able to see Commitment information.
- When a Commitment is created, the Commitment should be associated with the System Partner who created it.
- Only the users associated with a System Partner should be allowed to edit Commitments related to that System Partner
- Users with the role `Staff Member` or `NCFF Team Member` should be able to edit all Commitments.
- If a System Partner user is deleted, the Commitments associated with them should be reassigned to another user.

### Plan Actors
Plan Actors are the entities responsible for carrying out the work of the Statewide Plan for Community Well-Being at the community level, regionally, and statewide. Plan Actors include **Nebraska Children and Families Foundation** (abbreviated **NCFF Teams**), **Government Entities (referred to as **System Partners**), and **Community Collaboratives**.

## Development Guidelines

### Testing Strategy

#### Framework and Structure
- **Test Framework**: pytest with pytest-django
- **Test Organization**: 
  - Place tests in `tests/` directory within each app
  - Use descriptive test file names: `test_models.py`, `test_views.py`, `test_forms.py`, `test_permissions.py`
  - Group related tests in classes: `TestCommunityActionStep`, `TestPermissions`

#### Testing Requirements
- **Coverage Goal**: Aim for 80% code coverage for new features
- **Test Types**:
  - **Unit Tests**: Test models, forms, utilities in isolation
  - **Integration Tests**: Test views with permissions and database interactions
  - **Permission Tests**: Explicitly test all permission scenarios
- **Test Database**: Use separate test database with fixtures for consistent data

#### Test Commands
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov=users --cov-report=html

# Run specific test file
pytest core/tests/test_models.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_community_action"
```

#### Test Best Practices
- Use Django's `TestCase` for database tests, `SimpleTestCase` for non-database tests
- Create fixtures for common test data (users, goals, objectives)
- Test both success and failure paths
- Test permission boundaries explicitly
- Mock external dependencies
- Use factory_boy for complex test data generation

### Code Style and Quality

#### Code Formatting
- **Tool**: PyCharm Professional built-in formatter
- **Style Guide**: PEP 8 compliance
- **Line Length**: 120 characters maximum
- **Import Order**: 
  1. Standard library imports
  2. Django imports
  3. Third-party imports
  4. Local application imports

#### Documentation Standards
- **Docstrings**: Use Google-style docstrings for all public methods and classes
- **Type Hints**: Add type hints for function parameters and return values where beneficial
- **Comments**: Use inline comments sparingly, prefer self-documenting code
- **README Updates**: Document significant architectural changes

### Git Workflow

#### Branch Strategy
```
main                    # Production branch (protected)
├── develop            # Integration branch for features
├── feature/           # New features
│   ├── feature/add-user-notifications
│   └── feature/implement-data-export
├── fix/              # Bug fixes
│   ├── fix/community-action-permission-error
│   └── fix/duplicate-strategy-numbers
├── refactor/         # Code improvements without functionality changes
│   ├── refactor/optimize-dashboard-queries
│   └── refactor/consolidate-form-validation
├── test/             # Test additions or improvements
│   └── test/add-permission-tests
└── docs/             # Documentation updates
    └── docs/update-deployment-guide
```

#### Branch Naming Conventions
- `feature/descriptive-name` - New functionality
- `fix/issue-description` - Bug fixes
- `refactor/improvement-description` - Code improvements
- `test/test-description` - Test additions
- `docs/documentation-topic` - Documentation updates

#### Commit Message Format
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `test`: Adding tests
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `perf`: Performance improvements
- `chore`: Maintenance tasks

**Example:**
```
feat: add edit functionality for community action steps

- Added edit view with permission checking
- Created update form with validation
- Added edit button to dashboard
- Updated URLs and templates

Closes #123
```

#### Pull Request Process
1. Create feature branch from `develop`
2. Make changes following coding standards
3. Write/update tests
4. Ensure all tests pass
5. Update documentation if needed
6. Create PR to `develop` with description
7. Address review feedback
8. Merge after approval

### URL Patterns and View Organization

#### URL Naming Conventions
- Use snake_case for URL names: `community_activities`, `create_nc_activity`
- Use hyphens in URL paths: `/community-activities/`, `/create-nc-action-step/`
- Group related URLs logically
- Use UUID parameters for object identification
- Prefix AJAX endpoints with `ajax/`

#### URL Structure
```python
# List views
path('activities/', views.activities, name='activities'),

# Detail views  
path('activity/<uuid:activity_id>/', views.activity_details, name='activity_details'),

# Create views
path('create-community-activity/', views.create_community_activity, name='create_community_activity'),

# Edit views
path('community-activity/edit/<uuid:activity_id>/', views.edit_community_activity, name='edit_community_activity'),

# Delete views
path('community-activity/delete/<uuid:activity_id>/', views.delete_community_activity, name='delete_community_activity'),

# AJAX endpoints
path('ajax/load-objectives/', views.load_objectives, name='ajax_load_objectives'),
```

#### View Organization
- **Function-Based Views (FBVs)**: Current standard, keep using for consistency
- **Naming**: Use descriptive names matching URL patterns
- **Decorators**: Apply `@login_required` and permission decorators as needed
- **Error Handling**: Return appropriate HTTP responses (403, 404, etc.)
- **Context Data**: Pass minimal required data to templates

### Form Handling

#### Form Structure
- **ModelForms**: Use for database-backed forms
- **Form Widgets**: Customize with Bootstrap classes via widget attrs
- **Field Exclusion**: Exclude auto-generated fields (`activity_number`, `creator` fields)
- **Field Labels**: Customize using `label_from_instance` for related fields

#### Form Validation
```python
def clean_field_name(self):
    """Validate individual field"""
    value = self.cleaned_data.get('field_name')
    # Validation logic
    if not valid:
        raise forms.ValidationError("Error message")
    return value

def clean(self):
    """Cross-field validation"""
    cleaned_data = super().clean()
    # Validation logic
    return cleaned_data
```

#### Form Processing Pattern
```python
@login_required
@permission_required
def view_name(request):
    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            # Set additional fields
            instance.creator = request.user
            instance.save()
            messages.success(request, "Success message")
            return redirect('success_url')
    else:
        form = FormClass()
    
    return render(request, 'template.html', {'form': form})
```

### Data Migration Strategy

#### Migration Best Practices
1. **Always Review Auto-Generated Migrations**: Check for data loss risks
2. **Data Preservation**: When modifying fields:
   - Create new field
   - Migrate data
   - Remove old field
3. **Backwards Compatibility**: Ensure migrations can be reversed when possible
4. **Testing**: Test migrations on a copy of production data before deployment

#### Migration Workflow
```bash
# Create migrations after model changes
python manage.py makemigrations

# Review the migration file
# Check for RunPython operations that might affect data

# Test migration on development
python manage.py migrate

# Test rollback if needed
python manage.py migrate app_name migration_number
```

#### Data Safety Rules
- **Never delete fields with data** without explicit confirmation
- **Archive deleted records** instead of hard deleting when possible
- **Use `on_delete=SET_NULL`** for optional foreign keys
- **Use `on_delete=PROTECT`** for critical relationships
- **Document data migrations** in migration files

### Error Handling and Logging

#### Logging Configuration
```python
import logging

logger = logging.getLogger(__name__)

# Use in views/models
logger.info(f"User {user.id} created action step {action_step.id}")
logger.error(f"Failed to save commitment: {e}")
logger.warning(f"Deprecated method called: {method_name}")
```

#### Error Handling Patterns
```python
# View error handling
def view_name(request):
    try:
        # Main logic
        pass
    except Model.DoesNotExist:
        logger.warning(f"Object not found for user {request.user.id}")
        messages.error(request, "The requested item was not found.")
        return redirect('safe_fallback')
    except PermissionDenied:
        logger.warning(f"Permission denied for user {request.user.id}")
        return HttpResponseForbidden("You don't have permission to access this resource.")
    except Exception as e:
        logger.error(f"Unexpected error in view_name: {e}", exc_info=True)
        messages.error(request, "An unexpected error occurred. Please try again.")
        return redirect('safe_fallback')
```

#### User-Facing Messages
- **Success Messages**: Clear confirmation of actions
- **Error Messages**: User-friendly, actionable when possible
- **Validation Messages**: Specific field-level feedback
- **Permission Messages**: Clear explanation without revealing system details

```python
# Good examples
messages.success(request, "Your action step has been saved successfully.")
messages.error(request, "Please complete all required fields.")
messages.warning(request, "This action will be available after approval.")

# Avoid
messages.error(request, "Database constraint violation on foreign key.")
```

### Documentation Requirements

#### Code Documentation
1. **Module Docstrings**: Describe purpose and main components
2. **Class Docstrings**: Explain purpose, attributes, and usage
3. **Method Docstrings**: Document parameters, returns, raises
4. **Complex Logic**: Add inline comments for non-obvious code

#### Project Documentation
1. **README.md**: Keep updated with setup instructions
2. **CHANGELOG.md**: Document significant changes per release
3. **API Documentation**: Document any API endpoints
4. **Deployment Guide**: Maintain deployment procedures

#### Documentation Template
```python
"""
Module description explaining purpose and main functionality.
"""

class ClassName:
    """
    Brief description of the class purpose.
    
    Attributes:
        attribute_name: Description of attribute
    
    Example:
        >>> instance = ClassName()
        >>> instance.method()
    """
    
    def method_name(self, param1: str, param2: int = None) -> bool:
        """
        Brief description of what the method does.
        
        Args:
            param1: Description of param1
            param2: Description of param2 (optional)
            
        Returns:
            Description of return value
            
        Raises:
            ExceptionType: When this exception occurs
        """
        pass
```

### Development Priorities

1. **Critical Features First**: Focus on user-facing functionality
2. **Security Always**: Never compromise on authentication/authorization
3. **Test Critical Paths**: Ensure core workflows have test coverage
4. **Document as You Go**: Update documentation with changes
5. **Refactor Incrementally**: Improve code quality during feature work
6. **Performance When Needed**: Optimize only when issues arise (30 concurrent users max)

## Community Action Step Edit Functionality

### Implementation Status
The Community Action Step edit functionality is **fully implemented and tested** as of commit `5c92d1d`. This includes:

#### Core Components
- **Permission System** (`core/permissions.py`): Complete role-based access control
- **Edit Views** (`core/views.py`): Protected edit functionality with proper redirects
- **Forms** (`core/forms.py`): Full form with Community Collaborative dropdown
- **Templates**: Edit interface and UI integration across all relevant pages
- **Tests** (`core/tests/`): Comprehensive test suite covering all permission scenarios

#### User Interface Integration
Edit functionality is integrated into:
- **Individual Dashboard**: Edit buttons in actions column
- **My Community Activities**: Complete CRUD interface
- **Activity Details**: Edit button for authorized users
- **Community Activities List**: Edit buttons with permission checking

#### Permission Matrix
| User Type | Community Action Steps | NC Action Steps | System Partner Commitments |
|-----------|------------------------|-----------------|----------------------------|
| Anonymous | ❌ No Access | ❌ No Access | ❌ No Access |
| Community Collaborative | ✅ Own Collaborative Only | ❌ View Only | ❌ View Only |
| NCFF Team | ✅ All Action Steps | ✅ Own Work | ❌ View Only |
| System Partner | ❌ View Only | ❌ View Only | ✅ Own Commitments |
| Superuser | ✅ All | ✅ All | ✅ All |

### Known Issues and Solutions

#### Fixed Issues
1. **NCFF Team Permission Bug** (Fixed in commit `1894fe5`)
   - Issue: NCFF Team Members couldn't edit Community Action Steps
   - Solution: Added `user.member_type == user.MemberTypes.NCFF_TEAM` check to permission function

2. **Activity Details 404 Error** (Fixed in commit `df1aa4b`)
   - Issue: User-type-based routing caused 404s when viewing activity details
   - Solution: Changed to sequential model lookup instead of user-type-based filtering

3. **Missing Related Collaborative Field** (Fixed in commit `997ae3d`)
   - Issue: Edit form threw "required field" error for `related_collaborative`
   - Solution: Added dropdown field with proper widget and placeholder text

#### Current Implementation Details
- **Edit Flow**: Edit → Save → Activity Details (with success message) → User can verify changes
- **Navigation**: Back/Cancel buttons return to dashboard for consistent UX
- **Form Validation**: Comprehensive validation with user-friendly error messages
- **Security**: All endpoints protected with authentication and authorization decorators

## Testing Implementation

### Test Structure
Tests are organized in `core/tests/` directory following the guidelines in this document:

#### Test Files
- **`test_permissions.py`**: Permission function testing with all user scenarios
- **`test_visibility.py`**: Anonymous vs authenticated user access testing  
- **`test_views.py`**: View functionality and integration testing
- **`manual_test_runner.py`**: Environment-independent permission validation
- **`TEST_REPORT.md`**: Comprehensive compliance documentation

#### Test Coverage
All Community Action Step permission requirements from the Project Purpose section are tested:
- ✅ Action Steps visible to logged in users only
- ✅ Proper creator and collaborative association
- ✅ Collaborative-based edit permissions
- ✅ NCFF Team Members can edit all Community Action Steps
- ✅ Superuser full access
- ✅ UI permission enforcement

#### Running Tests
```bash
# Manual permission validation (works without Django environment)
python core/tests/manual_test_runner.py

# Full Django test suite (requires environment configuration)
python manage.py test core.tests

# Specific test files
python manage.py test core.tests.test_permissions
python manage.py test core.tests.test_visibility
python manage.py test core.tests.test_views
```

### Testing Best Practices Established
1. **Permission Testing**: Every permission scenario must be explicitly tested
2. **Manual Validation**: Use environment-independent tests for core logic validation
3. **Comprehensive Documentation**: Include test reports documenting CLAUDE.md compliance
4. **Bug Fix Validation**: Test fixes with both manual and automated tests

## Documentation Standards

### Knowledge Base Articles
Documentation is organized in `kb-articles/` directory:

#### Internal Documentation
- **`COMMUNITY_ACTION_STEP_WORKFLOW.md`**: Technical workflow documentation
- **Purpose**: Internal knowledge base for development team and staff
- **Content**: Complete user role workflows, technical implementation, troubleshooting

#### External Documentation  
- **`COMMUNITY_COLLABORATIVE_USER_GUIDE.md`**: End-user documentation
- **Purpose**: External knowledge base for Community Collaborative members
- **Format**: WikiJS-compatible with H1/H2/H3 structure
- **Style**: Beginner-friendly, non-technical language

### Documentation Requirements
1. **Dual Documentation**: Maintain both technical and user-facing documentation
2. **Screenshot Placeholders**: User guides should indicate where screenshots are needed
3. **Version Tracking**: Include document version and system version information
4. **Compliance Mapping**: Document how implementation meets CLAUDE.md requirements

## View and URL Patterns Established

### Community Action Step URLs
```python
# Established URL patterns for Community Action Steps
path('community-activity/edit/<uuid:activity_id>/', views.edit_community_activity, name='edit_community_activity'),
path('my-community-activities/', views.list_my_community_activities, name='list_my_community_activities'),
path('activity/<uuid:activity_id>/', views.activity_details, name='activity_details'),
path('community-activity/delete/<uuid:activity_id>/', views.delete_community_activity, name='delete_community_activity'),
```

### View Security Pattern
```python
# Standard security pattern for Community Action Step views
@login_required
@require_community_action_step_edit_permission
def edit_community_activity(request, action_step):
    """Edit view receives action_step from permission decorator"""
    # Implementation follows established pattern

@login_required  
def view_with_permission_checking(request):
    """Views add can_edit flags for UI permission display"""
    for activity in activities:
        activity.can_edit = has_community_action_step_edit_permission(user, activity)
```

### Template Integration Pattern
```html
<!-- Standard permission checking in templates -->
{% if activity.can_edit %}
    <a href="{% url 'edit_community_activity' activity.activity_id %}" class="btn btn-outline-primary btn-sm">
        <i class="bi bi-pencil"></i> Edit Action Step
    </a>
{% endif %}
```

## Development Workflow Patterns

### Feature Implementation Process
Based on Community Action Step implementation, establish this pattern for future features:

1. **Planning Phase**: 
   - Review CLAUDE.md requirements
   - Create implementation plan with TodoWrite tool
   - Identify permission requirements and user roles affected

2. **Implementation Phase**:
   - Implement core functionality (models, views, forms)
   - Add permission system integration
   - Update templates with UI elements
   - Follow established URL and view patterns

3. **Testing Phase**:
   - Create comprehensive test suite
   - Test all permission scenarios
   - Manual validation of core logic
   - Document test results and compliance

4. **Documentation Phase**:
   - Update CLAUDE.md if new patterns established
   - Create internal technical documentation
   - Create external user documentation if needed
   - Include screenshot placeholders for user guides

5. **Commit Strategy**:
   - Feature implementation commits
   - Bug fix commits (separate from features)
   - Test suite and documentation commits
   - Clear commit messages with 🤖 Claude Code attribution

### Integration Requirements
When adding new functionality that affects Community Action Steps:
1. **Maintain Permission Compatibility**: Use established permission functions
2. **Follow UI Patterns**: Use consistent button styles and permission checking
3. **Update Tests**: Add test coverage for any new permission scenarios
4. **Document Changes**: Update both internal and external documentation