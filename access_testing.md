# Secure Cricket Data Lake
## Access Testing Report

### Objective
To test login, MFA verification and role-based permissions for all four application roles.

### Test Results

| Test | Administrator | Data Analyst | Coach | Read-only User |
|---|---|---|---|---|
| Login with valid details | Pass | Pass | Pass | Pass |
| MFA verification | Pass | Pass | Pass | Pass |
| View Dashboard | Pass | Pass | Pass | Pass |
| Manage Users | Pass | Denied | Denied | Denied |
| Upload CSV Dataset | Denied | Pass | Blocked | Blocked |
| View Reports | Pass | Pass | Pass | Pass |
| Download Reports | Pass | Pass | Pass | Pass |

### Observations

1. The Administrator accessed user management and assigned roles.
2. The Data Analyst successfully uploaded cricket datasets.
3. The Coach accessed the dashboard and reports.
4. The Read-only User accessed the dashboard and reports.
5. The Coach and Read-only User were denied permission to upload datasets.
6. MFA verification was used during login.

### Conclusion

The tests confirmed that the application enforces role-based access for the tested operations. The Data Analyst can upload datasets, the Administrator can manage users, and the Coach and Read-only User have report access.
