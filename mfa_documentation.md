# Secure Cricket Data Lake
## Multi-Factor Authentication (MFA)

### Objective
To improve application security by requiring users to verify their identity using a time-based one-time password (TOTP).

### MFA Implementation
- Python library: PyOTP
- Authentication method: Time-Based One-Time Password (TOTP)
- Authenticator application: Google Authenticator
- MFA verification is required during login.

### User MFA Setup

| User | Role | MFA |
|---|---|---|
| swapna | Administrator | Enabled |
| analyst | Data Analyst | Enabled |
| coach | Coach | Enabled |
| viewer | Read-only User | Enabled |

### Login Security Process

1. User enters username.
2. User enters password.
3. User opens Google Authenticator.
4. User enters the current six-digit verification code.
5. The application verifies the code.
6. If the details are correct, the user can access the dashboard.

### Conclusion
MFA provides an additional layer of security beyond username and password authentication. It helps protect the Secure Cricket Data Lake application from unauthorized access.
