# LMS Backend API Documentation

## API Base URL

- Production: https://lms-backend-ioll.onrender.com/

## Interactive API Docs

If you install drf-yasg or drf-spectacular, you can access:
- Swagger UI: https://lms-backend-ioll.onrender.com/swagger/
- Redoc: https://lms-backend-ioll.onrender.com/redoc/

## Authentication

### POST `/api/auth/login/`
Login a user and obtain JWT access/refresh tokens.
- Request:
  ```json
  { "username": "user", "password": "pass" }
  ```
- Response:
  ```json
  {
    "access": "<jwt>",
    "refresh": "<jwt>",
    "user": {
        "id": 1,
        "username": "user",
        "first_name": "Test",
        "last_name": "User",
        "phone": "1234567890"
    }
  }
  ```

### POST `/api/token/`
This endpoint is still available for obtaining tokens, but `/api/auth/login/` is the primary login endpoint.
- Request:
  ```json
  { "username": "user", "password": "pass" }
  ```
- Response:
  ```json
  { "access": "<jwt>", "refresh": "<jwt>" }
  ```

### POST `/api/token/refresh/`
Refresh JWT access token.
- Request:
  ```json
  { "refresh": "<refresh_token>" }
  ```
- Response:
  ```json
  { "access": "..." }
  ```

### POST `/api/auth/register/`
Register new user (student or admin).
- Request:
  ```json
  { "username": "user", "email": "user@example.com", "password": "pass", "first_name": "Test", "last_name": "User" }
  ```
- Response:
  ```json
  { "id": 1, "username": "user", "first_name": "Test", "last_name": "User", "phone": null }
  ```

### POST `/auth/change-password/`
Change password (auth required).
- Request:
  ```json
  { "old_password": "old", "new_password": "new" }
  ```

### POST `/auth/logout/`
Logout and blacklist refresh token (auth required).
- Request:
  ```json
  { "refresh": "<refresh_token>" }
  ```

### POST `/auth/password-reset/`
Request password reset (email).
- Request:
  ```json
  { "email": "user@example.com" }
  ```

### POST `/auth/password-reset-confirm/`
Confirm password reset.
- Request:
  ```json
  { "uid": "<uidb64>", "token": "<token>", "new_password": "new" }
  ```

## Users & Profiles

### GET `/users/`
List users (auth required).
- Response:
  ```json
  [{ "id": 1, "username": "user", ... }]
  ```

### POST `/profiles/`
Create profile (auth required).
- Request:
  ```json
  { "user": 1, "nationality": "Kenyan", "national_id": "xxxx", ... }
  ```
- Response:
  ```json
  { "id": 1, "user": 1, ... }
  ```

## Courses

### GET `/courses/`
List courses (auth required).
- Response:
  ```json
  [{ "id": 1, "title": "Course Title", ... }]
  ```

### POST `/courses/`
Create course (auth required).
- Request:
  ```json
  { "title": "Course Title", "description": "...", ... }
  ```
- Response:
  ```json
  { "id": 1, "title": "Course Title", ... }
  ```

## File Uploads

### POST `/files/`
Upload file (auth required).
- Content-Type: multipart/form-data
- Request:
  ```
  file: <your_file>
  ```
- Response:
  ```json
  { "id": 1, "file": "url", ... }
  ```

## Notes

- All endpoints require trailing slashes (`/`).
- Use `Authorization: Bearer <access_token>` for protected endpoints.
- CORS is enabled for allowed origins.
- For full endpoint details, see backend code or request more examples.
