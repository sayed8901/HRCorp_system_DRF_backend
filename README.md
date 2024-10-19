# HRCorp Backend

## Project Description

**Project Type**: HR software  
**Project Name**: HRCorp

The backend of **HRCorp** is built using **Django** and **Django REST Framework** (DRF) to manage HR functionalities such as employee records, payroll, transfers, promotions, and more. The system allows multiple user management, where users are divided into `power_user` (admin) and `standard_user` (normal user). Power users have extended privileges to manage employee data and HR functionalities. The project uses PostgreSQL as the database.

---

<br>

## Technology Stack

- **Backend Framework**: Django, Django REST Framework
- **Database**: PostgreSQL (with superbase deployment)

---

<br>

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

<br>

## Instructions to Run Locally

### Prerequisites

- Python 3.12.2
- Django 4.2.4
- Django REST Framework 3.15.2
- PostgreSQL

### Packages used:

```bash
asgiref==3.8.1
certifi==2024.8.30
charset-normalizer==3.3.2
dj-database-url==2.2.0
dj-rest-auth==6.0.0
Django==4.2.4
django-allauth==0.63.3
django-cors-headers==4.4.0
django-environ==0.11.2
django-filter==24.3
djangorestframework==3.15.2
idna==3.10
Markdown==3.7
psycopg2-binary==2.9.9
python-dateutil==2.9.0.post0
requests==2.32.3
six==1.16.0
sqlparse==0.5.1
typing_extensions==4.12.2
tzdata==2024.2
urllib3==2.2.3
whitenoise==6.7.0
```

---

<br>

### Installation Steps

1. Open `command prompt` in the folder directory where you want to create & run the project locally

2. **Create a virtual environment**

   ```bash
   python -m venv hrcorp_env
   cd hrcorp_env
   Scripts\activate.bat
   ```

3. **Temporarily **Create a new project** named `HRCorp` to get the `SECRET_KEY`**

   ```bash
   django-admin startproject HRCorp
   ```

   <br>

4. **After creating a project named `HRCorp`,**

- Manually go to the project directory folder like: `...\hrcorp_env\HRCorp\HRCorp` to get the settings.py file.
- Rename that `settings.py` file to `temp_settings.py`
- Copy that `temp_settings.py` file and paste it to a temporary folder directory or in the root `hrcorp_env` directory

5. **Delete the project** created temporarily

- Go back to the root `hrcorp_env` directory
- Manually delete the temporarily created `HRCorp` project directory

<br>

6. Copy the `repository_url` to **Clone the repository**

   ```bash
   git clone https://github.com/sayed8901/HRCorp_system_DRF_backend.git
   ```

7. **Install dependencies**

   ```bash
   cd HRCorp_system_DRF_backend
   pip install -r requirements.txt
   code .
   ```

<br>

8. **Environment Variables Configuration**

- To run the application, you need to configure environment variables. Create a file named `.env` inside the root project directory of your project named `HRCorp`.

9. **Then, add the `SECRET_KEY` in that `.env` file:**

- Copy the secret key from the previously created temp_settings.py file
- for example --> `SECRET_KEY=django-insecure--se33_ik1yp+a%bz7a.....`

10. **Add the email sending accessibility credentials** in `.env` file:

- EMAIL: (Your email address for sending emails)
- EMAIL_PASSWORD: (Your email password or an app-specific password)

      - N.B.: please see the `### Note for: Email Setup` part for better understanding

<br>

11. **Also, Add the superbase postgreeSQL database credentials** in `.env` file:

- DB_NAME: (Your database name)
- DB_USER: (Your database username)
- DB_PASSWORD: (Your database password)
- DB_HOST: (The host for your database)
- DB_PORT: (The port for your database)

        - N.B.: please see the `### Note for: Database Setup` part for better understanding

<br>

12. **Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

13. **Creating superuser**

```bash
python manage.py createsuperuser
```

14. **Run the development server**

```bash
python manage.py runserver
```

<br>

15. **Finally, Access the application**

- Local: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

---

<br>

## Note for: Database Setup

1. **Setting up in Supabase:**

- Go to `supabase.com` and log in with your `GitHub` account.
- Navigate to the dashboard and click on **New project**.
  - Select your organization (e.g., `sayed8901’s Org`).
  - Provide a relevant project name (e.g., `hr_corp-db`).
  - Set a strong database password (consider using a password generator) and make sure to copy it, as you will need it later.
  - Choose the **Region** as **South Asia (Singapore)** and click **Create new project**.

2. **Updating settings.py:**

- Make sure to replace the default SQLite database settings with PostgreSQL settings in your `settings.py` file:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
    }
}
```

3. **Update the .env file:**

- In your .env file, replace/update the values for `DB_NAME`, `DB_USER`, `DB_HOST`, and `DB_PORT` based on your Supabase database configuration.
- You should also set `DB_PASSWORD` with the password you generated earlier.

```python
DB_NAME=postgres
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
```

**To find the required database connection details in Supabase:**

- Go to the `Supabase dashboard` and select your project.
- Choose the `database` option from the left sidebar.
- Alternatively, you can select the `connect` button from the top-right corner.
- Select the `Python` tab from the `Connection string`
- and go to `Connection parameters` for your database details.

---

<br>

## Note for: Email Setup

To set up email notifications for your Django application, follow these steps:

1. **Getting App Password**:

   - Log in to your `Google` account.
   - Click on your account profile image and select **Manage your Google Account**.
   - Navigate to the **Security** tab.
   - Enable **2-Step Verification** if it is not already enabled.
   - After enabling, scroll down and click on **App passwords**.
   - Provide an app name (e.g., `hrcorp`) and click **Create**. A `password` will be generated; copy this password;
   - paste this `password` onto the `EMAIL_PASSWORD` field in the `.env` file.

2. **Updating project settings.py**:

   - In your `settings.py` file, make sure to set up the email configuration as follows:

   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_USE_TLS = True
   EMAIL_PORT = 587
   EMAIL_HOST_USER = env("EMAIL")
   EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")
   ```

---

<br>

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

<br>

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

<br>

## Conclusion

In developing the **HRCorp** backend, I aimed to create a comprehensive solution for efficient HR management. Using Django and PostgreSQL, I built a scalable and secure platform that supports user management, employee tracking, and payroll processing.

I believe the features included will significantly enhance HR operations, and I'm excited for organizations to benefit from this tool. If you have questions or want to contribute, feel free to reach out!
