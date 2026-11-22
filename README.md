# Secure Cricket Data Lake

## Project Overview
The Secure Cricket Data Lake is a web-based application developed to store cricket match datasets and generate cricket statistics reports.

## Technologies Used
- VMware Workstation
- Ubuntu 24.04
- Python 3
- Flask
- SQLite Database
- CSV file storage
- PyOTP for MFA
- Google Authenticator

## Main Features
1. Secure user registration and login.
2. Multi-Factor Authentication.
3. Four application roles: Administrator, Data Analyst, Coach and Read-only User.
4. CSV dataset upload.
5. Raw and processed data storage.
6. Cricket statistics reports.
7. CSV report download.
8. Role-based access restrictions.
9. Administrator user management.

## Project Folder Structure

```text
Secure-Cricket-Data-Lake/
|
|-- app.py
|-- database.py
|-- requirements.txt
|-- architecture.md
|-- roles_permissions.md
|-- access_testing.md
|-- mfa_documentation.md
|-- README.md
|
|-- templates/
|   |-- login.html
|   |-- register.html
|   |-- setup_mfa.html
|   |-- dashboard.html
|   |-- upload.html
|   |-- reports.html
|   |-- admin.html
|
|-- data/
|   |-- raw-data/
|   |-- processed-data/
|   |-- reports/
|
|-- static/
```
## How to Run the Application

1. Open the project folder in Ubuntu Terminal.
2. Activate the Python virtual environment:

   `source venv/bin/activate`

3. Install required packages:

   `pip install -r requirements.txt`

4. Start the Flask application:

   `python app.py`

5. Open the browser and visit:

   `http://127.0.0.1:5000`

## Security

The application uses MFA and role-based access control. Only Data Analysts are allowed to upload datasets. The Administrator can manage users. Coaches and Read-only Users can view and download reports.

## Project Status

The application supports user login, MFA verification, CSV uploads, report generation, administrator user management and role-based access testing.
