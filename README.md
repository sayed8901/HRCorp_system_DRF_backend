# HRCorp Backend

## Project Description

**Project Type**: HR software  
**Project Name**: HRCorp

The backend of **HRCorp** is built using **Django** and **Django REST Framework** (DRF) to manage HR functionalities such as employee records, payroll, transfers, promotions, and more. The system allows multiple user management, where users are divided into `power_user` (admin) and `standard_user` (normal user). Power users have extended privileges to manage employee data and HR functionalities. The project uses PostgreSQL as the database.

---

## Technology Stack

- **Backend Framework**: Django, Django REST Framework
- **Database**: PostgreSQL (with superbase deployment)

---

## Project Features

### Multiple User Management

- Can have an admin user called “power_user.”
- Also can have multiple normal users called “standard_user.”

### User Authentication Management

- User registration.
- Email verification for confirmation link.
- Login & logout.

### Power_User Authorization Management

Only a “power_user” can:

- Create & update:
  - Designation
  - Department
  - Job Location
- Transfer modification:
  - Update an existing transfer record.
  - Cancel a transfer order.

### Employee Database Management

- Entry of new employees with relevant information such as personal info, employment info, salary info, separation info, etc.
- Implement salary structure with salary grading & stepping functionality.

### Employee Transfer Management

- Update job location after transferring an employee.
- Update job profile history accordingly.

### Employee Job Confirmation Management

- Update employee salary information after job confirmation.
- Update job profile history accordingly.

### Employee Promotion Management

- Update employee salary information after promotion.
- Update job profile history accordingly.

### Employee Separation Management

- Update employee separation data & change the employee status to “inactive.”
- Update job profile history accordingly.

### Employee Details View

- Get the full information of an employee on a single page (in a separate tab).

### Employee List View

- View all employee info in a table.
- Get employee list by:
  - Employee ID
  - Employee name
  - Department
  - Designation
  - Job location

### Reports Management

- Get a list of employees whose jobs need confirmation (up to this month).
- Get a list of employees who joined last month / filtered duration.
- Get a list of employees transferred last month / filtered duration.
- Get a list of employees separated last month / filtered duration.
- Get a list of employees whose jobs were confirmed last month / filtered duration.
- Get a list of employees promoted last month / filtered duration.

### HR Live Dashboard (for frontend homepage)

- Create an HR dashboard that displays statistical charts showing:
  - Number of active staff (by concerned departments).
  - Number of active staff (by concerned designations).
  - Number of active staff (by concerned job locations).

### Employee Leave Management

- Entry of leave data for an employee.
- Update “number of leave days status” for that employee.
- Deduct salary for Non-Paid Leave entries.
- Update payroll data accordingly.

### Payroll Management

- Prepare salary for the current month.
- Download salary sheet in PDF & XLSX format.

---

## Instructions to Run Locally

### Prerequisites

- Python 3.12.2
- Django 4.2.4
- Django REST Framework 3.15.2
- PostgreSQL

### Installation Steps

1. **Clone the repository**

   ```bash
    git clone <repository_url>
    cd HRCorp_HR_ERP_project
   ```

2. **Create a virtual environment**

   ```bash
    python -m venv django_env
    cd django_env
    Scripts\activate.bat
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
    python manage.py makemigrations
    python manage.py migrate
   ```

5. **Run the development server**

   ```bash
    python manage.py runserver
   ```

6. **Access the application**

   - Local: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

7. **Creating superuser**

   ```bash
    python manage.py createsuperuser
   ```

---

### Database Setup

The project is configured to use SQLite3 by default, but it can be switched to PostgreSQL. For PostgreSQL:

1. Install PostgreSQL and set up a database.

2. **Update the DATABASES setting in settings.py:**

   ```bash
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': '<your_db_name>',
            'USER': '<your_db_user>',
            'PASSWORD': '<your_db_password>',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
   ```

3. **Run migrations**

   ```bash
    python manage.py migrate
   ```

4. **Run the development server**

   ```bash
    python manage.py runserver
   ```

---

## Environment Variables Configuration

To run the application, you need to configure environment variables. Create a file named .env in the root directory of your project and add the following:

- SECRET_KEY: A unique key for cryptographic signing.

- EMAIL: Your email address for sending emails.
- EMAIL_PASSWORD: Your email password or an app-specific password.

- DB_NAME: Your database name.
- DB_USER: Your database username.
- DB_PASSWORD: Your database password.
- DB_HOST: The host for your database.
- DB_PORT: The port for your database.

Important: Ensure that you do not share this file or commit it to version control to protect sensitive information.

---

## API Endpoints

### User Management

- **Register Power User**:  
  `POST` - `/power_user/register/`  
  Allows creating a new Power User account.

- **Register Standard User**:  
  `POST` - `/standard_user/register/`  
  Allows creating a new Standard User account.

- **Login**:  
  `POST` - `/accounts/login/`  
  Authenticates a user and generates a session token.

- **Logout**:  
  `GET` - `/accounts/logout/`  
  Logs out the currently authenticated user.

- **User Account Data by User ID**:  
  `GET` - `/accounts/user/?user_id=<id>`  
  Retrieves the account details of a user by their ID.

- **Get Power User by User ID**:  
  `GET` - `/power_user/by_user_id/?user_id=<id>`  
  Retrieves a Power User's data by user ID.

- **Get Standard User by User ID**:  
  `GET` - `/standard_user/by_user_id/?user_id=<id>`  
  Retrieves a Standard User's data by user ID.

### Power User Management

- **List Power Users**:  
  `GET` - `/power_user/list/`  
  Returns a list of all Power Users.

- **Update/Delete Power User by ID**:  
  `GET`/`PUT`/`PATCH`/`DELETE` - `/power_user/list/<id>/`  
  Allows retrieving, updating, or deleting a Power User by their ID.

### Standard User Management

- **List Standard Users**:  
  `GET` - `/standard_user/list/`  
  Returns a list of all Standard Users.

- **Update/Delete Standard User by ID**:  
  `GET`/`PUT`/`PATCH`/`DELETE` - `/standard_user/list/<id>/`  
  Allows retrieving, updating, or deleting a Standard User by their ID.

### Department Management (Power User Only)

- **Create Department**:  
  `POST` - `/employment/departments/`  
  Allows a Power User to create a department.

- **Retrieve/Update/Delete Department by ID**:  
  `GET`/`PUT`/`PATCH`/`DELETE` - `/employment/departments/<id>/`  
  Allows retrieving, updating, or deleting a department by its ID.

### Designation Management (Power User Only)

- **Create Designation**:  
  `POST` - `/employment/designations/`  
  Allows a Power User to create a designation.

- **Retrieve/Update/Delete Designation by ID**:  
  `GET`/`PUT`/`PATCH`/`DELETE` - `/employment/designations/<id>/`  
  Allows retrieving, updating, or deleting a designation by its ID.

### Job Location Management (Power User Only)

- **Create Job Location**:  
  `POST` - `/employment/job_locations/`  
  Allows a Power User to create a job location.

- **Retrieve/Update/Delete Job Location by ID**:  
  `GET`/`PUT`/`PATCH`/`DELETE` - `/employment/job_locations/<id>/`  
  Allows retrieving, updating, or deleting a job location by its ID.

### Employee Management

- **List Employees**:  
  `GET` - `/employee/list/`  
  Returns a list of all employees.

- **Create Employee**:  
  `POST` - `/employee/list/`  
  Allows creating a new employee.

- **Get Full Info of All Employees**:  
  `GET` - `/employee/all-info/`  
  Retrieves comprehensive information for all employees.

- **Delete Employee by ID** (Power User Only):  
  `DELETE` - `/employee/list/<id>/`  
  Deletes an employee by their ID.

### Employee Personal Information

- **List All Personal Info**:  
  `GET` - `/employment/personal_info/list/`  
  Returns a list of all personal information.

- **Get/Update Employee Personal Info by Employee ID**:  
  `GET`/`PUT` - `/employment/personal_info/?employee_id=<id>`  
  Retrieves or updates the personal info of an employee by their employee ID.

### Employee Employment Information

- **List All Employment Info**:  
  `GET` - `/employment/employment_info/list/`  
  Returns a list of all employment information.

- **Get/Update Employee Employment Info by Employee ID**:  
  `GET`/`PUT` - `/employment/employment_info/?employee_id=<id>`  
  Retrieves or updates the employment info of an employee by their employee ID.

### Salary Information

- **List All Salary Info**:  
  `GET` - `/salary/salary_info/list/`  
  Returns a list of all salary information.

- **Get/Update Employee Salary Info by Employee ID**:  
  `GET`/`PUT` - `/salary/salary_info/?employee_id=<id>`  
  Retrieves or updates the salary info of an employee by their employee ID.

### Job Profile History

- **Get Employee Job Profile History by Employee ID**:  
  `GET` - `/job_profile_history/?employee_id=<id>`  
  Retrieves the job profile history of an employee by their employee ID.

- **List All Job Profile Histories**:  
  `GET` - `/job_profile_history/list/`  
  Returns a list of all employee job profile histories.

### Employee Transfer

- **List All Employee Transfers**:  
  `GET` - `/transfer/list/`  
  Returns a list of all employee transfers.

- **Get/Create Employee Transfer by Employee ID**:  
  `GET`/`POST` - `/transfer/?employee_id=<id>`  
  Retrieves or creates a transfer record for an employee by their employee ID.

- **Update Employee Transfer by Transfer ID (Power User Only)**:  
  `PUT` - `/transfer/update/?transfer_id=<id>`  
  Updates the transfer info of an employee by the transfer ID.

- **Delete Employee Transfer by Transfer ID (Power User Only)**:  
  `DELETE` - `/transfer/cancel/?transfer_id=<id>`  
  Deletes an employee's last transfer record by the transfer ID.

### Job Confirmation

- **Confirm Employee Job**:  
  `POST` - `/confirmation/confirm/?employee_id=<id>`  
  Confirms the job of an employee by their employee ID.

- **List All Job Confirmations**:  
  `GET` - `/confirmation/list/`  
  Returns a list of all job confirmations.

### Employee Promotion

- **Promote Employee**:  
  `POST` - `/promotion/promote/?employee_id=<id>`  
  Promotes an employee by their employee ID.

- **Get All Promotions of an Employee**:  
  `GET` - `/promotion/promote/?employee_id=<id>`  
  Retrieves all promotion records of an employee by their employee ID.

- **List All Promotions**:  
  `GET` - `/promotion/list/`  
  Returns a list of all promotions.

### Employee Separation

- **Separate an Employee**:  
  `POST` - `/separation/deactivate/?employee_id=<id>`  
  Deactivates (separates) an employee by their employee ID.

- **List All Separations**:  
  `GET` - `/separation/list/`  
  Returns a list of all employee separations.

### Employee Leave Management

- **List All Employee Leave Info**:  
  `GET` - `/leave/list/`  
  Returns a list of all employee leave records.

- **Get/Create Employee Leave by Employee ID**:  
  `GET`/`POST` - `/leave/?employee_id=<id>`  
  Retrieves or creates a leave record for an employee by their employee ID.

- **Update Employee Leave by Leave ID (Power User Only)**:  
  `PUT` - `/leave/update/?leave_id=<id>`  
  Updates a leave record for an employee by the leave ID.

- **Delete Employee Leave by Leave ID (Power User Only)**:  
  `DELETE` - `/leave/cancel/?leave_id=<id>`  
  Deletes a leave record for an employee by the leave ID.

### Payroll Processing

- **Process Payroll for a Particular Month**:  
  `GET` - `/payroll/process_payroll/?month=<YYYY-MM>`  
  Processes payroll for all employees for the specified month.

- **Get/Update/Delete Employee Payroll by Payroll ID (Power User Only)**:  
  `GET`/`PUT`/`DELETE` - `/payroll/payroll/<id>/`  
  Retrieves, updates, or deletes a payroll record for an employee by the payroll ID.

---

## Sample requests for model schemas:

### Create New Employee : POST

```bash
 {
     "personal_info_data":
     {
         "name": "Md. Sayed Hossain",
         "gender": "Male",
         "father_name": "Md. Habibur Rahman",
         "mother_name": "Hasina Begum",
         "marital_status": "Single",
         "spouse_name": "",
         "permanent_address": "Uzirpur, Barishal",
         "present_address": "Sastapur, Fatullah, Narayanganj",
         "date_of_birth": "1992-04-12",
         "smart_id": "123",
         "contact_number": "01915158901",
         "email": "sayed91515@gmail.com",
         "educational_degree": "MBA",
         "blood_group": "AB+"
     },
     "employment_info_data":
     {
         "joining_date": "2024-09-01",
         "probation_period_months": 1,
         "job_location": "Zone-1",
         "department": "Finance & Accounts",
         "designation": "Officer"
     },
     "salary_info_data":
     {
         "salary_grade": 8,
         "salary_step": 3
     }
 }
```

### Employment_info : PUT

```bash
 {
 "status": "Active",
 "joining_date": "2024-08-01",
 "probation_period_months": 1
 }
```

### Create transfer info : POST, PUT

```bash
 {
 "transfer_from_location": "Head Office",
 "transfer_from_department": "HR & Admin",
 "transfer_to_location": "Branch-002",
 "transfer_to_department": "Sales",
 "transfer_effective_date": "2024-08-28"
 }
```

### Create leave info : POST, PUT

```bash
 {
 "leave_type": "Non_Paid_Leave",
 "leave_start_date": "2024-09-11",
 "leave_end_date": "2024-09-13"
 }
```

---

## Conclusion

In developing the **HRCorp** backend, I aimed to create a comprehensive solution for efficient HR management. Using Django and PostgreSQL, I built a scalable and secure platform that supports user management, employee tracking, and payroll processing.

I believe the features included will significantly enhance HR operations, and I'm excited for organizations to benefit from this tool. If you have questions or want to contribute, feel free to reach out!
