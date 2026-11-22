
# Secure Cricket Data Lake Architecture

## 1. Project Overview

The Secure Cricket Data Lake is developed using VMware Workstation and Ubuntu 24.04. It stores cricket match datasets and provides secure access to analytics reports.

## 2. System Architecture

```text
             Users
               |
               v
       Flask Web Application
               |
               v
       Registration and Login
               |
               v
       Multi-Factor Authentication
          (PyOTP and QR Code)
               |
               v
        Role-Based Access Control
               |
       +-------+--------+
       |       |        |
       v       v        v
 Administrator Analyst Coach
               |
          Read-only User
               |
               v
       Application Services
       /        |          \
      v         v           v
   Upload    Dashboard    Reports
      |                     |
      v                     v
   Raw Data             CSV Download
      |
      v
   Processed Data

   SQLite Database
   (Users, Password Hashes,
    Roles and MFA Secrets)
```

## 3. Storage Structure

The project uses local storage inside the Ubuntu virtual machine.

- Raw Data: Original uploaded cricket CSV files.
- Processed Data: Processed cricket datasets.
- Reports: Downloadable cricket analytics reports.
- SQLite Database: User account and access information.

## 4. Technologies Used

- VMware Workstation
- Ubuntu 24.04
- Python 3
- Flask Web Framework
- SQLite Database
- CSV Dataset Storage
- PyOTP for Multi-Factor Authentication
- QR Code Generation

## 5. Security Features

- Username and password authentication.
- Multi-Factor Authentication.
- Administrator user management.
- Role-Based Access Control.
- Restricted dataset uploads.
- Read-only report access.
- Password hashing in the user database.

## 6. User Roles

- Administrator: Manages users and assigns roles.
- Data Analyst: Uploads cricket datasets.
- Coach: Views analytics reports.
- Read-only User: Views available reports.

## 7. Project Deployment

The application runs locally inside Ubuntu 24.04 using VMware Workstation. Flask provides the web interface, SQLite stores user information, and local VM folders store cricket datasets and reports.
