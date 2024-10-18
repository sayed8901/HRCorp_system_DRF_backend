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

## API Endpoints

### User Management

- **Register Power User**  
  `POST /power_user/register/`

- **Register Standard User**  
  `POST /standard_user/register/`

- **Login**  
  `POST /accounts/login/`

- **Logout**  
  `GET /accounts/logout/`

- **Get User Account Data**  
  `GET /accounts/user/?user_id=<id>`

- **Get Power User Data by User ID**  
  `GET /power_user/by_user_id/?user_id=<id>`

- **Get Standard User Data by User ID**  
  `GET /standard_user/by_user_id/?user_id=<id>`

---

### Employee Management

- **Create New Employee**  
  `POST /employee/list/`

- **Get All Employees**  
  `GET /employee/list/`

- **Get Employee by ID**  
  `GET /employee/list/<employee_id>/`

- **Delete Employee** (only by power user)  
  `DELETE /employee/list/<employee_id>/`

- **Update Employee Personal Info**  
  `GET /employment/personal_info/?employee_id=<id>`  
  `PUT /employment/personal_info/?employee_id=<id>`

- **Update Employee Employment Info**  
  `GET /employment/employment_info/?employee_id=<id>`  
  `PUT /employment/employment_info/?employee_id=<id>`

- **Update Employee Salary Info**  
  `GET /salary/salary_info/?employee_id=<id>`  
  `PUT /salary/salary_info/?employee_id=<id>`

---

### Job Profile Management

- **Get Job Profile History by Employee ID**  
  `GET /job_profile_history/?employee_id=<id>`

- **Get All Employee Job Profiles**  
  `GET /job_profile_history/list/`

---

### Transfer Management

- **Get All Transfers**  
  `GET /transfer/list/`

- **Get Transfer by Employee ID**  
  `GET /transfer/?employee_id=<id>`

- **Update Transfer Info by Transfer ID** (only by power user)  
  `PUT /transfer/update/?transfer_id=<id>`

- **Cancel Transfer by Transfer ID** (only by power user)  
  `DELETE /transfer/cancel/?transfer_id=<id>`

---

### Promotion and Confirmation Management

- **Make Job Confirmation**  
  `POST /confirmation/confirm/?employee_id=<id>`

- **Get All Job Confirmations**  
  `GET /confirmation/list/`

- **Make Promotion**  
  `POST /promotion/promote/?employee_id=<id>`

- **Get All Promotions**  
  `GET /promotion/list/`

---

### Separation Management

- **Make Separation**  
  `POST /separation/deactivate/?employee_id=<id>`

- **Get All Separations**  
  `GET /separation/list/`

---

### Leave Management

- **Get All Leave Records**  
  `GET /leave/list/`

- **Get Individual Leave Record by Employee ID**  
  `GET /leave/?employee_id=<id>`

- **Update Leave Record by Leave ID** (only by power user)  
  `PUT /leave/update/?leave_id=<id>`

- **Cancel Leave Record by Leave ID** (only by power user)  
  `DELETE /leave/cancel/?leave_id=<id>`

---

### Payroll Management

- **Process Payroll for a Specific Month**  
  `GET /payroll/process_payroll/?month=<YYYY-MM>`

- **Get Payroll Info by Payroll ID**  
  `GET /payroll/payroll/<payroll_id>/`  
  `PUT /payroll/payroll/<payroll_id>/`  
  `DELETE /payroll/payroll/<payroll_id>/`

---

## Instructions to Run Locally

### Prerequisites

- Python 3.x
- Django 4.x
- Django REST Framework 3.x
- SQLite3 (or PostgreSQL for production)

### Installation Steps

1. **Clone the repository**

   ```bash
    git clone <repository_url>
    cd HRCorp_HR_ERP_project
   ```

2. **Create a virtual environment**

   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
    python manage.py migrate
   ```

5. **Run the development server**

   ```bash
    python manage.py runserver
   ```

6. **Access the application**

   Local: http://127.0.0.1:8000/
   Admin Panel: http://127.0.0.1:8000/admin/

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

### Power User Features

- **List Power Users**:  
  `GET` - `/power_user/list/`  
  Returns a list of all Power Users.

- **Update/Delete Power User by ID**:  
  `PUT`/`PATCH`/`DELETE` - `/power_user/list/<id>/`  
  Allows updating or deleting a Power User by their ID.

### Standard User Features

- **List Standard Users**:  
  `GET` - `/standard_user/list/`  
  Returns a list of all Standard Users.

- **Update/Delete Standard User by ID**:  
  `PUT`/`PATCH`/`DELETE` - `/standard_user/list/<id>/`  
  Allows updating or deleting a Standard User by their ID.

### Employee Management

- **List Employees**:  
  `GET` - `/employee/list/`  
  Returns a list of all employees.

- **Create Employee**:  
  `POST` - `/employee/list/`  
  Allows the creation of a new employee.

- **Get Full Info of All Employees**:  
  `GET` - `/employee/all-info/`  
  Retrieves comprehensive information for all employees.

- **Delete Employee by ID**:  
  `DELETE` - `/employee/list/<id>/`  
  Deletes an employee by their ID.

### Department, Designation & Job Location Management

- **Create Department**:  
  `POST` - `/employment/departments/`  
  Creates a new department.

- **Update/Delete Department by ID**:  
  `PUT`/`PATCH`/`DELETE` - `/employment/departments/<id>/`  
  Updates or deletes a department by its ID.

- **Create Designation**:  
  `POST` - `/employment/designations/`  
  Creates a new designation.

- **Update/Delete Designation by ID**:  
  `PUT`/`PATCH`/`DELETE` - `/employment/designations/<id>/`  
  Updates or deletes a designation by its ID.

- **Create Job Location**:  
  `POST` - `/employment/job_locations/`  
  Creates a new job location.

- **Update/Delete Job Location by ID**:  
  `PUT`/`PATCH`/`DELETE` - `/employment/job_locations/<id>/`  
  Updates or deletes a job location by its ID.

### Salary & Payroll Management

- **List All Salary Info**:  
  `GET` - `/salary/salary_info/list/`  
  Retrieves a list of all salary information records.

- **Get Salary Info by Employee ID**:  
  `GET` - `/salary/salary_info/?employee_id=<id>`  
  Returns salary information for a specific employee by their ID.

- **Process Payroll for a Particular Month**:  
  `GET` - `/payroll/process_payroll/?month=<YYYY-MM>`  
  Generates payroll for the specified month.

- **Get/Update/Delete Payroll by ID**:  
  `GET`/`PUT`/`DELETE` - `/payroll/payroll/<id>/`  
  Retrieves, updates, or deletes a payroll record by its ID.

## Sample requests for model schemas:

### Create New Employee : POST

{
"personal_info_data": {
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
"blood_group": "AB+",
},
"employment_info_data": {
"joining_date": "2024-09-01",
"probation_period_months": 1,
"job_location": "Zone-1",
"department": "Finance & Accounts",
"designation": "Officer",
},
"salary_info_data": {
"salary_grade": 8,
"salary_step": 3,
}
}

### Employment_info : PUT

{
"status": "Active",
"joining_date": "2024-08-01",
"probation_period_months": 1
}

### Create transfer info : POST, PUT

{
"transfer_from_location": "Head Office",
"transfer_from_department": "HR & Admin",
"transfer_to_location": "Branch-002",
"transfer_to_department": "Sales",
"transfer_effective_date": "2024-08-28"
}

### Create leave info : POST, PUT

{
"leave_type": "Non_Paid_Leave",
"leave_start_date": "2024-09-11",
"leave_end_date": "2024-09-13"
}
