# Community Action Step Workflow by User Role

## Overview

This document outlines the complete Community Action Step workflow based on different user roles in the Statewide Plan for Community Well-Being Portal. The system implements role-based access control to ensure users can only view and edit action steps they are authorized to access.

## User Role Definitions

### User Types
- **Anonymous Users**: Not logged into the system
- **Community Collaborative Users**: Members of specific Community Collaboratives
- **NCFF Team Members**: Staff members of Nebraska Children and Families Foundation
- **System Partners**: Government entities and system partners
- **Superusers**: System administrators with full access

---

## Detailed Workflow by User Role

### 🚫 Anonymous Users (Not Logged In)

**Access Level**: ❌ **No Access**

#### Restrictions:
- **Cannot see any action step information** (complies with CLAUDE.md requirement)
- **Redirected to login page** when attempting to access:
  - Activity details pages
  - Community activities lists
  - Individual dashboard
  - My activities page
  - Any edit functionality

#### Security:
All action step information is protected and requires authentication. This ensures sensitive collaborative work remains secure.

---

### 🏘️ Community Collaborative Users

**Access Level**: 🔒 **Limited - Own Collaborative Only**

#### Viewing Permissions:
- ✅ **Community Action Steps from their own collaborative**
- ✅ **Community Action Steps they personally created**
- ❌ **Community Action Steps from other collaboratives**
- ✅ **NC Action Steps** (view only)
- ✅ **System Partner Commitments** (view only)

#### Editing Permissions:
- ✅ **Action steps they personally created**
- ✅ **Action steps from their collaborative (created by other members)**
- ❌ **Action steps from other collaboratives**
- ❌ **NC Action Steps**
- ❌ **System Partner Commitments**

#### User Interface Elements:
- **Edit buttons appear** on action steps they can edit
- **Delete buttons appear** only on action steps they created
- **View buttons** appear on all accessible action steps
- **No edit buttons** on action steps from other collaboratives

#### Available Pages:
1. **Individual Dashboard**
   - Shows action steps they created
   - Edit and view buttons in actions column
   - Quick overview of their work

2. **My Community Activities**
   - Comprehensive list of their collaborative's action steps
   - Full CRUD operations (Create, Read, Update, Delete)
   - Table view with action buttons

3. **Community Activities List**
   - Browse action steps by strategy
   - Edit buttons appear for authorized action steps
   - Filtered view by collaborative

4. **Activity Details**
   - Detailed view of individual action steps
   - Edit button appears if user has permission
   - Success messages after editing

#### Edit Workflow:
1. **Access Edit Form** via dashboard, my activities, or activity details
2. **Fill Out Form** with activity details and select collaborative
3. **Save Changes** - validates and saves to database
4. **Success Confirmation** - redirected to activity details with success message
5. **Verification** - user can immediately see changes reflected

---

### 🏢 NCFF Team Members (Staff Members)

**Access Level**: 🔓 **Full Access - All Community Action Steps**

#### Viewing Permissions:
- ✅ **All Community Action Steps** (regardless of collaborative)
- ✅ **All NC Action Steps** (their own work area)
- ✅ **System Partner Commitments** (view only)

#### Editing Permissions:
- ✅ **All Community Action Steps** (from any collaborative)
- ✅ **Their own NC Action Steps**
- ❌ **System Partner Commitments** (different permission system)

#### Special Privileges:
- **Oversight Role**: Can edit action steps from any collaborative
- **Quality Assurance**: Can review and modify community work
- **Support Role**: Can help communities with their action steps
- **Cross-Collaborative Access**: Can switch between collaboratives when editing

#### User Interface Elements:
- **Edit buttons appear** on all Community Action Steps
- **Full access** to edit forms
- **Can change collaborative assignment** in dropdown
- **Administrative capabilities**

#### Workflow:
1. **Dashboard Access** - See action steps from all collaboratives
2. **Universal Edit Access** - Edit buttons appear on all Community Action Steps
3. **Quality Control** - Can review and improve community work
4. **Support Communities** - Can assist with action step management
5. **Cross-Collaborative Management** - Can reassign action steps if needed

---

### 🏛️ System Partners (Government Entities)

**Access Level**: 🔒 **Limited - Own Commitments + View Only**

#### Viewing Permissions:
- ✅ **Community Action Steps** (view only - no edit access)
- ✅ **NC Action Steps** (view only)
- ✅ **Their own System Partner Commitments**

#### Editing Permissions:
- ❌ **Community Action Steps** (cannot edit)
- ❌ **NC Action Steps** (cannot edit)
- ✅ **Their own System Partner Commitments** (separate system)

#### User Interface Elements:
- **No edit buttons** appear on Community Action Steps
- **View-only access** to community and NC work
- **Cannot access** Community Action Step edit forms
- **Focus on their own commitment system**

#### Workflow:
1. **Browse Community Work** - Can view Community Action Steps for context
2. **Monitor Progress** - See how community work aligns with their commitments
3. **No Editing** - Cannot modify community action steps
4. **Own Commitment System** - Manage their own System Partner Commitments separately

---

### 👑 Superusers (System Administrators)

**Access Level**: 🔓 **Full Access - Everything**

#### Permissions:
- ✅ **All Community Action Steps** (full CRUD access)
- ✅ **All NC Action Steps** (full CRUD access)
- ✅ **All System Partner Commitments** (full CRUD access)
- ✅ **Administrative functions**
- ✅ **User management capabilities**

#### Workflow:
- **Complete Administrative Access** to all action steps
- **Edit buttons appear everywhere** they have permissions
- **Can manage any user's work**
- **System maintenance and oversight**
- **Data integrity and quality control**

---

## Common Edit Workflow (for Authorized Users)

### Entry Points:
Users can access the edit form from multiple locations:

1. **Individual Dashboard** → Click edit icon (pencil) in actions column
2. **My Community Activities** → Click "Edit" button in actions column
3. **Activity Details Page** → Click "Edit Action Step" button
4. **Community Activities List** → Click "Edit Action Step" button

### Edit Process:

#### Step 1: Permission Verification
- System automatically verifies user has permission to edit this action step
- Unauthorized users receive 403 Forbidden error
- Authorization based on user role and action step ownership

#### Step 2: Edit Form Display
User sees pre-populated form containing:
- **Activity Name** (text input)
- **Activity Details** (textarea)
- **Activity Lead** (text input)
- **Community Collaborative** (dropdown with "-- Select Your Collaborative --" placeholder)
- **Status** (dropdown: Not Started, In Progress, Completed, Ongoing)
- **Completion Year** (dropdown)
- **Completion Quarter** (dropdown: Q1, Q2, Q3, Q4)
- **Plan Alignment** (read-only section showing Goal, Objective, Strategy)

#### Step 3: Form Submission
- User fills out form and clicks "Save Changes"
- Form validates all required fields
- System saves changes to database
- Creator and collaborative associations maintained

#### Step 4: Success Confirmation
- User redirected to **Activity Details page**
- **Success message** appears: "Community action step updated successfully!"
- User can immediately verify their changes were saved

#### Step 5: Verification
- Updated information displays on activity details page
- User can confirm edits were properly saved to database
- Changes visible across all views of the action step

### Navigation Options:

#### During Editing:
- **Back to Dashboard** → Returns to user's individual dashboard
- **Cancel** → Returns to dashboard without saving changes

#### After Saving:
- **Automatic Redirect** → Taken to activity details page to verify changes
- **Edit Button Still Available** → Can make additional edits if needed
- **Dashboard Access** → Can return to dashboard to see updated information

---

## Security and Permission Summary

### Authentication Requirements:
- **All action step functionality requires login**
- **Anonymous users cannot access any action step information**
- **Automatic redirect to login page** for unauthorized access attempts

### Authorization Hierarchy:
1. **Community Collaborative Users**: Limited to own collaborative
2. **NCFF Team Members**: Full access to all Community Action Steps
3. **System Partners**: View-only access to Community Action Steps
4. **Superusers**: Full administrative access to everything

### User Interface Security:
- **Edit buttons only appear** for users with edit permissions
- **Forms reject unauthorized access** with HTTP 403 errors
- **Permission checking at every access level**
- **No sensitive information exposed** to unauthorized users

### Data Integrity:
- **Action steps properly associated** with creator and collaborative
- **Audit trail maintained** through creator and timestamp fields
- **Form validation ensures** all required fields are completed
- **Database constraints prevent** invalid data entry

---

## Technical Implementation Notes

### Permission System:
- Implemented in `core/permissions.py`
- Function: `has_community_action_step_edit_permission(user, action_step)`
- Decorator: `@require_community_action_step_edit_permission`

### View Security:
- All views protected with `@login_required` decorator
- Permission checks added to view functions
- UI elements conditionally displayed based on `can_edit` flags

### Database Design:
- Action steps linked to both creator and collaborative
- UUID-based primary keys for security
- Proper foreign key relationships with cascading rules

---

## Troubleshooting

### Common Issues:

#### "This field is required" errors:
- Ensure Community Collaborative dropdown is selected
- All required fields must be completed before saving

#### 404 errors on activity details:
- Fixed in latest implementation
- System now searches across all activity types
- Contact administrator if issues persist

#### Permission denied errors:
- User may not have appropriate role for editing
- Check user's collaborative assignment
- Verify user is logged in with correct account

### Support:
For technical issues or questions about the Community Action Step workflow, contact the development team or system administrators.

---

## Version Information

**Document Version**: 1.0  
**Last Updated**: January 2025  
**System Version**: Based on implementation in commit df1aa4b  
**Compliance**: Fully compliant with CLAUDE.md requirements

---

*This document is part of the Statewide Plan for Community Well-Being Portal internal knowledge base and should be updated as system functionality evolves.*