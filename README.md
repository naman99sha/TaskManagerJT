# Task Management API

## Overview

This project is a Django-based Task Management API that allows users to create tasks, assign tasks to users, and retrieve tasks assigned to specific users.

## Features

- User Registration with Token Authentication
- Task Creation
- Task Assignment to Multiple Users
- Fetching Tasks Assigned to a Specific User

---

## Setup and Installation

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.8+
- Django
- Django REST Framework
- SQLite3 (or any other database configured in Django settings)

### Installation Steps

1. **Clone the Repository**

   ```sh
   git clone https://github.com/naman99sha/TaskManagerJT.git
   cd TaskManagerJT
   ```

2. **Create a Virtual Environment**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```sh
   cd ../../
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser (Optional)**

   ```sh
   python manage.py createsuperuser
   ```

   Follow the prompts to create an admin user.

6. **Run the Server**

   ```sh
   python manage.py runserver
   ```

---

## API Endpoints

### 1. User Registration

**Endpoint:** `POST /task/api/register/`

**Request:**

```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "mobile": "1234567890"
}
```

**Response:**

```json
{
    "token": "abc123xyz",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "mobile": "1234567890"
    }
}
```

---

### 2. User Login (Get Auth Token)

**Endpoint:** `POST /task/api/api-token-auth/`

**Request:**

```json
{
    "username": "testuser",
    "password": "password123"
}
```

**Response:**

```json
{
    "token": "abc123xyz"
}
```

---

### 3. Create a Task

**Endpoint:** `POST /task/api/tasks/`

**Headers:**

```sh
(To be passed in request header)
Authorization: Token abc123xyz
```

**Request:**

```json
{
    "name": "Complete API Documentation",
    "description": "Write the README file for the API",
    "task_type": "documentation",
    "status": "pending"
}
```

**Response:**

```json
{
    "id": 1,
    "name": "Complete API Documentation",
    "description": "Write the README file for the API",
    "task_type": "documentation",
    "status": "pending"
}
```

---

### 4. Assign Task to Users

**Endpoint:** `POST /task/api/tasks/{task_id}/assign/`

**Headers:**

```sh
Authorization: Token abc123xyz
```

**Request:**

```json
{
    "user_ids": [2, 3]
}
```

**Response:**

```json
{
    "status": "Users assigned successfully"
}
```

---

### 5. Get Tasks Assigned to Logged-in User

**Endpoint:** `GET /task/api/tasks/my_tasks/`

**Headers:**

```sh
Authorization: Token abc123xyz
```

**Response:**

```json
[
    {
        "id": 1,
        "name": "Complete API Documentation",
        "description": "Write the README file for the API",
        "task_type": "documentation",
        "status": "pending",
        "assigned_users": [{"id": 2, "username": "user1"}, {"id": 3, "username": "user2"}]
    }
]
```

---

## Running Tests

To run tests, execute the following command:

```sh
python manage.py test
```

---

## Test Credentials

Use these credentials for testing (if you created a superuser, use those instead):

- **Username:** `testuser`
- **Password:** `password123`
- **Auth Token:** Generated after registration/login

---

## Conclusion

This API provides essential task management features, ensuring proper authentication and role-based task assignment. Future improvements could include:

- Task due dates and priorities
- Enhanced user permissions and roles
- Notifications for assigned tasks

