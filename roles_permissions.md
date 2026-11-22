# Secure Cricket Data Lake

## Application Roles and Permissions

| Feature | Administrator | Data Analyst | Coach | Read-only User |
|---|---|---|---|---|
| Login | Allowed | Allowed | Allowed | Allowed |
| MFA Verification | Required | Required | Required | Required |
| View Dashboard | Allowed | Allowed | Allowed | Allowed |
| Manage Users | Allowed | Denied | Denied | Denied |
| Upload CSV Dataset | Denied | Allowed | Denied | Denied |
| View Cricket Reports | Allowed | Allowed | Allowed | Allowed |
| Download Reports | Allowed | Allowed | Allowed | Allowed |

## Role Description

### 1. Administrator
The Administrator can log in using MFA, access the dashboard, manage user accounts and assign roles.

### 2. Data Analyst
The Data Analyst can log in using MFA, view the dashboard, upload cricket datasets, view reports and download reports.

### 3. Coach
The Coach can log in using MFA, view the dashboard, access cricket reports and download reports. Upload permission is restricted.

### 4. Read-only User
The Read-only User can log in using MFA, view the dashboard, access reports and download reports. Dataset uploads are not permitted.

## Security Implementation

The application uses Flask session management and role-based access control. Only users with the Data Analyst role can upload CSV datasets. Only the Administrator can manage users. All roles must complete MFA verification during login.

Note: These are application-level roles implemented in the Ubuntu VM, not AWS IAM roles.
