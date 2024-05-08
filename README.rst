===============
Project Team Module
===============

Description
-----------

The "Project Team" module enhances project management in Odoo by introducing a new model called project.team.member with various functionalities. Below are the details of the functionalities implemented in this module:

1. **Project Team Member Model**:
   - Fields:
     - Name
     - Address (with subfields: House no., Street, Street2, Country, State, City, Zip code)
     - Mobile
     - User_id (Many2one res.users)
     - Email (related to user_id.email)
     - Gender
     - Birth date
     - User Image (Binary)
     - Bio Data (HTML)
     - Active (Boolean)
     - Timesheet (One2many account.analytic.line)
   - Views: Form view, Tree view, Search view, Kanban view

2. **User Creation**:
   - A new user is created when a project.team.member is created.

3. **Record Copy Restriction**:
   - Users are restricted from copying records.

4. **Dropdown Options in User_id Field**:
   - Dropdown options display the name along with the email of the user.

5. **Project Team Model**:
   - Fields:
     - Team_members (Many2many project.team.member)
     - Name
     - Team_leader
     - Active
     - Sequence char (Readonly, Copy=False)
   - Views: Form view, Tree view, Kanban view, Activity view
   - Order by name with description added

6. **Chatter and Activity in Form View**:
   - Chatter and activity are added in the form view, with tracking enabled on 2 fields.

7. **Smart Button**:
   - A smart button in the project.team form view displays the number of assigned team members.

8. **Add Member to Multiple Teams**:
   - A server action "Add Member" opens a wizard to add a new member to multiple teams selected from the team tree view.

9. **Project Configuration Menu**:
   - Added a menu in the project configuration to add teams.

10. **Project Team Assignment**:
    - Selected teams from project configuration are added to the project and displayed in the kanban view under the Team page.

11. **Access Rights**:
    - Access rights are set for new models to restrict visibility and operations.

12. **Task Assignment Restriction**:
    - Users can only see tasks assigned to them. Assigned Date is added to project.task, and past dates are not allowed.

13. **Task Search View Filter**:
    - Added a filter named "New tasks" with a domain as Worked hour < 5 in the search view of project.task.

14. **Task Priority Assignment**:
    - Users can assign priority to multiple tasks by selecting them from the task list view.

15. **Timesheet Entries**:
    - Timesheet entries created by employees in tasks are also added to project team members.

16. **Demo Data**:
    - Two demo data records are added to the module.

17. **Language Translation**:
    - Gujarati language is loaded, and five terms are translated. The name of project.team is translated to Gujarati.

18. **Description Tab**:
    - A new tab "Description" is added in the Project form view with a new field "description" with text type and index.

Instructions
------------

Please follow the instructions below to achieve the functionalities mentioned above:

1. Inherit project.team.
2. Create team members many2many field in project.team with relation to project.team.member.
3. Inherit Project.project:
   - Put many2one team id of project.team with domain of project.
   - Put members named many2many field with relation to project.team.member.
4. Inherit project.task and add Assigned Date (Datetime field).
5. Override create and write methods to handle date validation and unlink restriction.
6. Inherit search_view of project.task and add a new filter named "New tasks".
7. Implement task priority assignment for multiple tasks.
8. Add timesheet entries to project team members from tasks.
9. Set access rights for new models.
10. Translate terms and project.team name to Gujarati.
11. Add a new tab "Description" in the Project form view with a new field "description" with text type and index.

