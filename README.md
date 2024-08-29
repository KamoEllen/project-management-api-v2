<!--https://final-api-fr66.onrender.com/docs
-->
### Why I Chose Specific Packages and Development Experience

This is my third Python API project this week, and my choices were shaped by past experiences and project requirements.

# Check out this video:

[![Watch the video](https://github.com/KamoEllen/project-management-api-v2/blob/main/Thumbnail.png?raw=true)](https://www.youtube.com/watch?v=Ha-FUmVgB5o)

<!--
![img](https://github.com/KamoEllen/Final-API/blob/main/img.png?raw=true)
-->

### **Current Features Checklist**

#### **Authentication and Authorization**
- [x] Token-based authentication with JWT
- [x] User registration
- [x] Secure password hashing with `bcrypt`
- [x] Token expiration management

#### **User Management**
- [x] Create a new user
- [x] Retrieve user details by ID
- [x] Update user details
- [x] Delete a user

#### **Milestone Management**
- [x] Create a new milestone
- [x] Retrieve milestones with pagination
- [x] Retrieve a single milestone by ID
- [x] Update a milestone by ID
- [x] Delete a milestone by ID

#### **Task Management**
- [x] Create a new task
- [x] Retrieve tasks with pagination
- [x] Retrieve a single task by ID
- [x] Update a task by ID
- [x] Delete a task by ID

#### **Progress Tracking**
- [x] Create a new progress entry
- [x] Retrieve progress entries by user ID
- [x] Retrieve a single progress entry by ID

#### **Error Handling**
- [x] Standard HTTP status codes for errors
- [x] Custom error messages for clarity

### **Future Improvements**

#### **Authentication and Authorization**
- [ ] Implement multi-factor authentication (MFA)
- [ ] Add OAuth2 support for third-party integrations
- [ ] Enhance token security with refresh tokens

#### **Task Management**
- [ ] Implement task prioritization and deadlines
- [ ] Add task dependencies and subtasks
- [ ] Enable task comments or notes


**1. Package Selection:**

- **FastAPI**: I chose it for its speed and built-in Swagger UI, which is great for interactive design and customization. It's now my go-to framework, as it also handles the front-end aspects I need.

- **Pydantic**: Used for data validation because it integrates well with FastAPI and simplifies handling data models.

- **Motor**: Selected for asynchronous MongoDB operations. Initially, I faced dependency issues, which were resolved by upgrading to Python 3.11.

- **Passlib**: Chosen for secure password hashing and management.

**2. Development Challenges:**

- **Dependency Issues**: Resolved by upgrading to Python 3.11, which fixed compatibility problems with Motor.

- **Project Rebuild**: Started from scratch after an earlier project failed due to outdated dependencies. This allowed me to apply improved practices.

Previous Projects:**
- **[First API](https://github.com/KamoEllen/OAuth-Project-Tracker)**: Works well and is deployed on render , too basic.
- **[Second API](https://github.com/KamoEllen/api)**: Works well , was deployed , crashed . 

**3. Personal Motivation and Future Plans:**

- **Personal Use**: Inspired by my daily use of Notion.io, I wanted a private place to manage and document my projects securely.

- **Future Enhancements**: Plans include adding advanced security features, such as better authentication and data encryption.


# Project Management API

## Overview

The **Project Management API** is a FastAPI-based application designed to facilitate the management of projects, milestones, tasks, and progress tracking. This API allows users to create, read, update, and delete data related to projects, milestones, tasks, and user progress. It also includes user authentication to ensure secure access to endpoints.

## Features

- **User Authentication**: Secure login and token-based authentication.
- **Project Management**: Endpoints to manage projects, milestones, tasks, and track progress.
- **CRUD Operations**: Full support for Create, Read, Update, and Delete operations.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Setup and Installation](#setup-and-installation)
3. [Configuration](#configuration)
4. [API Endpoints](#api-endpoints)
   - [User Endpoints](#user-endpoints)
   - [Milestones Endpoints](#milestones-endpoints)
   - [Tasks Endpoints](#tasks-endpoints)
   - [Progress Endpoints](#progress-endpoints)
5. [Testing](#testing)
6. [Contributing](#contributing)
7. [License](#license)

## Getting Started

This API is built using FastAPI and MongoDB. To get started with the Project Management API, follow the instructions below.

## Setup and Installation

### Prerequisites

- Python 3.8+
- MongoDB
- `pip` for installing Python packages

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/project-management-api.git
   cd project-management-api
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Environment**

   Create a `.env` file in the root directory of the project with the following content:

   ```env
   MONGODB_URI=mongodb://localhost:27017
   ```

5. **Run the Application**

   ```bash
   uvicorn app.main:app --reload
   ```

   The application will start and be accessible at `http://127.0.0.1:8000`.

## Configuration

Configuration settings are loaded from the `.env` file. Make sure to adjust the MongoDB connection URI according to your environment.

## API Endpoints

### User Endpoints

#### `POST /token`

- **Description**: Authenticates a user and returns an access token.
- **Request Body**: 
  ```json
  {
    "username": "user",
    "password": "pass"
  }
  ```
- **Response**: 
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

#### `POST /users/`

- **Description**: Registers a new user.
- **Request Body**:
  ```json
  {
    "username": "user",
    "password": "pass"
  }
  ```
- **Response**:
  ```json
  {
    "id": "user_id",
    "username": "user"
  }
  ```

#### `GET /users/{user_id}`

- **Description**: Retrieves a user's details.
- **Response**:
  ```json
  {
    "id": "user_id",
    "username": "user"
  }
  ```

#### `PUT /users/{user_id}`

- **Description**: Updates user details.
- **Request Body**:
  ```json
  {
    "username": "new_user",
    "password": "new_pass"
  }
  ```
- **Response**:
  ```json
  {
    "id": "user_id",
    "username": "new_user"
  }
  ```

#### `DELETE /users/{user_id}`

- **Description**: Deletes a user.
- **Response**:
  ```json
  {
    "status": "User deleted"
  }
  ```

### Milestones Endpoints

#### `POST /milestoness/`

- **Description**: Creates a new milestone.
- **Request Body**:
  ```json
  {
    "milestone_string": "string",
    "project_id": "string",
    "task_id": "string"
  }
  ```
- **Response**:
  ```json
  {
    "milestone_id": "milestone_id",
    "milestone_string": "string",
    "project_id": "string",
    "task_id": "string"
  }
  ```

#### `GET /milestoness/`

- **Description**: Retrieves a list of milestones with pagination.
- **Query Parameters**: `skip`, `limit`
- **Response**:
  ```json
  [
    {
    "milestone_id": "milestone_id",
    "milestone_string": "string",
    "project_id": "string",
    "task_id": "string"
    }
  ]
  ```

#### `GET /milestoness/{id}`

- **Description**: Retrieves a single milestone by ID.
- **Response**:
  ```json
  {
    "milestone_id": "milestone_id",
    "milestone_string": "string",
    "project_id": "string",
    "task_id": "string"
  }
  ```

#### `PUT /milestoness/{id}`

- **Description**: Updates a milestone by ID.
- **Request Body**:
  ```json
  {
    "milestone_id": "milestone_id",
    "milestone_string": "string",
  }
  ```
- **Response**:
  ```json
  {
    "milestone_id": "milestone_id",
    "milestone_string": "string",
    "project_id": "string",
    "task_id": "string"
  }
  ```

#### `DELETE /milestoness/{id}`

- **Description**: Deletes a milestone by ID.
- **Response**:
  ```json
  {
    "message": "Milestone deleted successfully"
  }
  ```

### Tasks Endpoints

#### `POST /taskss/`

- **Description**: Creates a new task.
- **Request Body**:
  ```json
  {
    "project_id": "string",
    "task_description": "string"
  }
  ```
- **Response**:
  ```json
  {
    "project_id": "string",
    "task_description": "string",
    "id": "string",
    "user_id": "string"
  }
  ```

#### `GET /taskss/`

- **Description**: Retrieves a list of tasks with pagination.
- **Query Parameters**: `skip`, `limit`
- **Response**:
  ```json
  [
    {
      "task_description": "string",
      "id": "string",
      "user_id": "string"
    }
  ]
  ```

#### `GET /taskss/{id}`

- **Description**: Retrieves a single task by ID.
- **Response**:
  ```json
  {
    "task_id": "string",

  }
  ```

#### `PUT /taskss/{id}`

- **Description**: Updates a task by ID.
- **Request Body**:
  ```json
  {
    "task_id": "string",
  }
  ```
- **Response**:
  ```json
  {
    "project_id": "string",
    "task_description": "string",
    "id": "string",
    "user_id": "string"
  }
  ```

#### `DELETE /taskss/{id}`

- **Description**: Deletes a task by ID.
- **Response**:
  ```json
  {
    "message": "Task deleted successfully"
  }
  ```

### Progress Endpoints

#### `POST /progress/`

- **Description**: Creates a new progress entry.
- **Request Body**:
  ```json
  {
    
  "title": "string",
  "content": "string",
  "rating": 0,
  "userId": "string"

  }
  ```
- **Response**:
  ```json
  {
    "title": "string",
    "content": "string",
    "rating": 0,
    "id": "string",
    "user_id": "string"
  }
  ```

#### `GET /progress/user/{user_id}`

- **Description**: Retrieves progress entries by user ID.
- **Response**:
  ```json
  [
    {
       "title": "string",
      "content": "string",
      "rating": 0,
      "id": "string",
      "user_id": "string"
      
    }
  ]
  ```

### Progress Endpoints (continued)

#### `GET /progress/{progress_id}`

- **Description**: Retrieves a single progress entry by ID.
- **Response**:
  ```json
  {
    "title": "string",
    "content": "string",
    "rating": 0,
    "id": "string",
    "user_id": "string"
  }
  ```

## User Endpoints

### Authentication

#### `POST /token`

- **Description**: This endpoint allows users to login and receive an access token.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```
- **Notes**: The access token is valid for 30 minutes. It must be included in the `Authorization` header as a Bearer token for authenticated requests.

### User Management

#### `POST /users/`

- **Description**: This endpoint allows new users to register.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "id": "string",
    "username": "string"
  }
  ```
- **Errors**:
  - `400 Bad Request`: If the username is already registered.

#### `GET /users/{user_id}`

- **Description**: Get details of a specific user.
- **Path Parameter**:
  - `user_id`: ID of the user to retrieve.
- **Response**:
  ```json
  {
    "id": "string",
    "username": "string"
  }
  ```
- **Errors**:
  - `404 Not Found`: If the user is not found.

#### `PUT /users/{user_id}`

- **Description**: Update user details.
- **Path Parameter**:
  - `user_id`: ID of the user to update.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "id": "string",
    "username": "string"
  }
  ```
- **Errors**:
  - `404 Not Found`: If the user is not found.

#### `DELETE /users/{user_id}`

- **Description**: Delete a user.
- **Path Parameter**:
  - `user_id`: ID of the user to delete.
- **Response**:
  ```json
  {
    "status": "User deleted"
  }
  ```
- **Errors**:
  - `404 Not Found`: If the user is not found.

## Authentication and Authorization

### Security

The API uses JWT (JSON Web Tokens) for authentication. Users must obtain a token by logging in with their credentials. The token should be included in the `Authorization` header as a Bearer token for all subsequent requests that require authentication.

### Password Management

Passwords are hashed using the `bcrypt` algorithm before being stored in the database. Passwords are never stored in plain text.

### Token Management

Tokens are created with a default expiration time of 15 minutes, which can be extended to 30 minutes on login. Tokens are validated on each request to ensure they are still valid.

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests:

- `200 OK`: The request was successful, and the server responded with the requested data.
- `201 Created`: The request was successful, and a new resource was created.
- `400 Bad Request`: The request could not be understood or was missing required parameters.
- `401 Unauthorized`: Authentication credentials were missing or invalid.
- `404 Not Found`: The requested resource could not be found.
- `500 Internal Server Error`: An error occurred on the server.

## Testing

To ensure the API functions correctly, it's recommended to write and run tests. The project uses the `pytest` framework for testing.

### Running Tests

1. **Install Testing Dependencies**

   If not already installed, you can add `pytest` to your environment:

   ```bash
   pip install pytest
   ```

2. **Run Tests**

   Navigate to the root directory of your project and run:

   ```bash
   pytest
   ```

   This will execute all test cases and provide a report of passed and failed tests.

## Contributing

We welcome contributions to the Project Management API! If you'd like to contribute, please follow these steps:

1. **Fork the Repository**

   Click the "Fork" button at the top right of this repository page.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/kamoellen/project-management-api-v2.git
   cd project-management-api
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature-branch
   ```

4. **Make Your Changes**

   Implement your changes or new features.

5. **Commit Your Changes**

   ```bash
   git add .
   git commit -m "Add your commit message"
   ```

6. **Push Your Changes**

   ```bash
   git push origin 
   ```

7. **Create a Pull Request**

   Go to the repository on GitHub and create a Pull Request from your forked repository's branch.

For detailed information on how to contribute, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

<!-- ## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

--- -->

## Challenges and Solutions

<details>
<summary>1. Authentication and Authorization</summary>
<p>
**Challenge:** Securely managing user authentication and authorization.<br>
**Solution:** 
- Used JWTs for secure token-based authentication.<br>
- Implemented password hashing with `bcrypt` for secure storage.
</p>
</details>

<details>
<summary>2. Data Validation</summary>
<p>
**Challenge:** Ensuring accurate and secure data handling.<br>
**Solution:** 
- Leveraged Pydantic models for validation and serialization.<br>
- Added custom error handling for clear responses.
</p>
</details>

<details>
<summary>3. Database Performance</summary>
<p>
**Challenge:** Efficiently managing and scaling database operations.<br>
**Solution:** 
- Utilized asynchronous operations with `Motor`.<br>
- Implemented indexing for faster queries.
</p>
</details>

<details>
<summary>4. Error Handling</summary>
<p>
**Challenge:** Properly identifying and managing errors.<br>
**Solution:** 
- Used HTTP status codes for error reporting.<br>
- Integrated logging for detailed error tracking.
</p>
</details>

<details>
<summary>5. User Data Security</summary>
<p>
**Challenge:** Securing user data and managing user operations.<br>
**Solution:** 
- Applied access controls for sensitive operations.<br>
- Ensured data sanitization to prevent vulnerabilities.
</p>
</details>

<details>
<summary>6. Code Quality</summary>
<p>
**Challenge:** Keeping the codebase maintainable and well-documented.<br>
**Solution:** 
- Conducted code reviews for consistency.<br>
- Provided comprehensive API documentation.
</p>
</details>


