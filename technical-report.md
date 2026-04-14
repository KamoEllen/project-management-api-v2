# Technical Report: Project Management API v2

---

## Table of Contents

1. [Summary](#1-summary)
2. [Purpose and Requirements](#2-purpose-and-requirements)
   - 2.1 [The Need for JWT Authentication](#21-the-need-for-jwt-authentication)
   - 2.2 [System Rules](#22-system-rules)
3. [System Design and Choices](#3-system-design-and-choices)
   - 3.1 [Data Identifiers](#31-data-identifiers)
   - 3.2 [Organising the Code](#32-organising-the-code)
   - 3.3 [Handling Concurrent Requests](#33-handling-concurrent-requests)
4. [Comparing Different Methods](#4-comparing-different-methods)
   - 4.1 [Persistent Storage vs. In-Memory Storage](#41-persistent-storage-vs-in-memory-storage)
   - 4.2 [Token Expiry: Fixed Window vs. Sliding Window](#42-token-expiry-fixed-window-vs-sliding-window)
   - 4.3 [Test Environments: Live Atlas vs. Local Database](#43-test-environments-live-atlas-vs-local-database)
5. [Testing and Results](#5-testing-and-results)
   - 5.1 [What the Current Tests Cover](#51-what-the-current-tests-cover)
   - 5.2 [Test Coverage Gaps](#52-test-coverage-gaps)
6. [Access and Security](#6-access-and-security)
   - 6.1 [User Roles](#61-user-roles)
   - 6.2 [Login Security](#62-login-security)
7. [Conclusion](#7-conclusion)

---

## 1. Summary

The Project Management API v2 is a Python backend service that stores and retrieves records for projects, milestones, tasks, and user progress. It exposes those records over HTTP using a REST interface.

The system is built on **FastAPI**, a Python web framework that runs on the ASGI standard, meaning it can process multiple HTTP requests at the same time without starting one thread per request. Data for milestones, users, progress entries, and projects is stored in a **MongoDB** database hosted on Atlas, accessed through **Motor**, which is MongoDB's official async Python driver. Task records are stored differently — in a Python dictionary that lives in the server's memory rather than in MongoDB.

Authentication works through **JWT** (JSON Web Tokens). A client that provides a correct username and password receives a signed token. All protected routes check that token before returning any data. Passwords for registered users are hashed with **bcrypt** before storage, so the database never holds a readable password.

The specific problems the system addresses are: keeping a structured record of which tasks belong to which project, which milestones a project contains, and what progress a given user has made on their assigned tasks — all behind a single authentication layer.

---

## 2. Purpose and Requirements

### 2.1 The Need for JWT Authentication

Without an authentication layer, any HTTP client that knows a URL can read or delete any record in the system. A project management tool holds records that belong to specific users — a user's task assignments, their progress entries, their account details. Returning those records to any caller without checking who the caller is would make the data meaningless as a management tool.

JWT authentication solves this by issuing a signed string (the token) after a successful login. The server signs the token with a secret key using the HMAC-SHA256 algorithm. Any later request that includes that token can be verified by the server without consulting the database on every call — the server re-computes the signature and checks it matches. If someone alters the token's contents (for example, changing the `sub` field to a different username), the signature no longer matches and the server rejects the request with a 401 status.

The token also carries an expiry timestamp in its payload (`exp` field). Once that time passes, the server refuses the token even if the signature is valid. This limits how long a stolen token can be used.

### 2.2 System Rules

The system enforces the following constraints:

- A request to any protected endpoint without a token, or with an expired or malformed token, receives an HTTP 401 response with the message `"Could not validate credentials. The token may be invalid or expired."` No data is returned.
- A token whose `sub` field does not match the registered username is also rejected with a 401, with the message `"User associated with the token does not exist. Please re-authenticate."`
- Passwords are not stored in plain text. When a user is created via `POST /users/`, the password field is passed through `get_password_hash()` in `utils.py` before the document is written to MongoDB. The stored value is a bcrypt hash string, not the original password.
- List endpoints for milestones and tasks accept `skip` and `limit` query parameters. If neither is provided, the default is to skip 0 records and return at most 10.

---

## 3. System Design and Choices

### 3.1 Data Identifiers

The system uses two different formats for record IDs depending on which storage layer is involved. Understanding the difference matters because the two formats are not interchangeable, and mixing them up causes the API to return a 500 error rather than a clear 400 Bad Request.

**BSON ObjectId** — used for milestones, users, progress entries, and projects stored in MongoDB. A BSON ObjectId is 12 bytes long. The first 4 bytes are a Unix timestamp (the number of seconds since 1 January 1970), which means ObjectIds sort roughly in the order they were created. The next 5 bytes are a random value generated once per process. The last 3 bytes are an incrementing counter that starts at a random number. When the model helper functions return an ID to the caller (for example, `milestones_helper()` in `app/models/milestones.py`), they call `str(milestones["_id"])`, which converts those 12 bytes to a 24-character lowercase hex string such as `507f1f77bcf86cd799439011`.

If a caller sends a different string to an endpoint that expects a MongoDB ObjectId — for example, a 36-character UUID4 string — the call to `ObjectId(id)` inside the model function raises a `bson.errors.InvalidId` exception. The current code catches this as a generic `Exception` and re-raises it as an error string, which FastAPI returns as a 500 Internal Server Error. The caller receives no indication that the problem was a malformed ID.

**UUID4** — used for task records stored in the in-memory dictionary `TASK_DATA` in `app/models/tasks.py`. A UUID4 is 128 bits of random data, written as a 36-character string in the format `xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx`, for example `550e8400-e29b-41d4-a716-446655440000`. Python's `uuid.uuid4()` generates this value. Unlike an ObjectId, a UUID4 has no timestamp component and carries no information about when the record was created.

The practical consequence of the split: a `task_id` field on a milestone record holds a UUID4 string, but the milestone document itself is stored in MongoDB and identified by an ObjectId. Any query that tries to look up a milestone using a task's UUID4 as if it were an ObjectId will fail with an `InvalidId` exception.

### 3.2 Organising the Code

The code is split into three layers that each have one job.

```
app/
├── main.py          ← registers routers, configures middleware
├── database.py      ← opens the MongoDB connection, exposes collections
├── models/          ← Pydantic schemas + all database read/write functions
└── routes/          ← HTTP endpoint definitions, request/response handling
```

The `routes/` files receive an HTTP request, validate the incoming data using Pydantic models, call the relevant function in `models/`, and return the result. They do not contain any database queries directly. The `models/` files contain all the logic for reading and writing records but do not know anything about HTTP status codes or request formats. The `database.py` file does one thing: opens an `AsyncIOMotorClient` connection to Atlas and exposes the five collections (`projects`, `tasks`, `milestones`, `users`, `progress`) as module-level variables that the model files import.

This separation means that changing how a record is stored — for example, moving task storage from the in-memory dictionary to MongoDB — only requires changes in `app/models/tasks.py` and `app/database.py`. The route file `app/routes/tasks.py` would not need to change.

### 3.3 Handling Concurrent Requests

FastAPI runs on ASGI, which means a single server process can handle multiple requests at the same time. When a request hits an `await` expression — for example, `await milestones_collection.insert_one(milestones_dict)` in `create_milestones()` — the server pauses that request and runs another one while waiting for MongoDB to respond. This is different from a threaded server, where each request occupies a thread for its entire duration.

For MongoDB operations this works correctly because Motor is an async driver. It can hold multiple open connections to the database and return results to whichever request is waiting for them.

For the in-memory `TASK_DATA` dictionary, the situation is different. There is no `await` inside `create_tasks()` — the function reads and writes the dictionary synchronously. Two simultaneous `POST /taskss/` requests will both generate a UUID4, write to the dictionary, and return without either waiting for the other. Python's Global Interpreter Lock prevents two threads from running Python bytecode at the exact same instant, so the dictionary itself will not become corrupted. But neither write is acknowledged by any durable storage. If the server process is restarted — whether by a crash, a deployment, or a scale-down event — both records are gone.

A concrete example: User A creates the task "Design the homepage" and User B simultaneously creates "Write the copy." Both receive successful 200 responses with their task IDs. One minute later the server restarts. `GET /taskss/{id}` for either task returns nothing, because `TASK_DATA` is an empty dictionary again at startup. The same two operations against MongoDB would survive the restart because Motor waits for the database to confirm the write before the `await` returns.

---

## 4. Comparing Different Methods

### 4.1 Persistent Storage vs. In-Memory Storage

The milestone and user routes store records in MongoDB. The task routes store records in a Python dictionary (`TASK_DATA`) declared at module level in `app/models/tasks.py`. These two approaches have different properties.

A MongoDB write is durable. Once `insert_one()` returns an `inserted_id`, the record exists in the database regardless of what happens to the server process. A dictionary write exists only in the memory of the running process. Any event that ends the process — a crash, a deployment update, an operating system restart — empties the dictionary.

Additionally, if the API were ever scaled to run on more than one server instance (for example, two Uvicorn workers behind a load balancer), each instance would have its own separate copy of `TASK_DATA`. A task created on instance A would be invisible to instance B. MongoDB, being a separate service, is shared by all instances.

The in-memory approach is faster for individual operations — writing to a Python dictionary takes microseconds while a MongoDB round-trip to Atlas takes 50–150 milliseconds. For a development prototype this trade-off is acceptable. For a production system where task records need to survive restarts and be readable by any server instance, the dictionary would need to be replaced with a proper database collection.

### 4.2 Token Expiry: Fixed Window vs. Sliding Window

The token expiry constant in `app/routes/auth.py` is:

```python
ACCESS_TOKEN_EXPIRE_MINUTES = 300
```

300 minutes is 5 hours. The README states that tokens expire in 15–30 minutes. These two values describe different security postures.

A 15-to-30-minute window means a stolen token can only be used for a short time before it expires. The user must log in more frequently, but the exposure window is small. A 5-hour window is more convenient — the user stays logged in across a typical working day — but a stolen token remains valid for up to 5 hours after it is taken.

A fixed expiry window (as implemented here) starts counting from the moment the token is issued and does not reset when the user makes requests. A sliding window would reset the expiry on every valid request, keeping an active user logged in indefinitely while still expiring tokens for inactive sessions. The current system uses the fixed approach.

### 4.3 Test Environments: Live Atlas vs. Local Database

The database connection string in `app/database.py` points directly to a live Atlas cluster, including credentials written in plain text in the source file. When `pytest` runs, any test that exercises a database route writes to and reads from that live cluster.

A live Atlas connection during tests has three specific problems that a local database instance does not:

**No isolation.** Tests that write documents to the live cluster leave those documents in the database when the test ends. If a test fails halfway through, partial records remain. The next test run may read those leftover records and produce unexpected results. A local MongoDB instance, started fresh before each test run, begins with an empty database every time.

**Network dependency.** Each database operation in a test requires a round-trip to Atlas over the internet. A single operation takes 50–150 milliseconds on a good connection. A test suite with 40 database operations takes roughly 4–6 seconds on network alone. The same suite against a local MongoDB instance, where a round-trip takes under 1 millisecond, runs in under 1 second. This gap grows as the test suite grows.

**Credentials in source code.** The connection string in `database.py` line 4 contains a username and password in plain text. Any person who reads the source file has access to the database. An environment variable (e.g. `MONGO_DETAILS = os.getenv("MONGO_DETAILS")`) would keep the credential out of version control. A local test database would require no credential at all.

---

## 5. Testing and Results

### 5.1 What the Current Tests Cover

The repository includes a `pytest` test suite. The tests target the HTTP endpoints through FastAPI's `TestClient`, which sends requests to the application without starting a real server. This covers the full path from HTTP request to database operation to HTTP response for each tested route.

The routes tested include milestone creation, retrieval by ID, list retrieval with pagination, update, and delete. User registration and the token endpoint are also covered. These tests verify that the correct HTTP status codes are returned and that the response body matches the expected structure.

### 5.2 Test Coverage Gaps

The task routes use `TASK_DATA` — the in-memory dictionary — rather than MongoDB. Tests for these routes do pass, because the dictionary is populated correctly during the test run. However, the tests do not verify the behaviour that a real MongoDB write would produce.

Specifically: the tests do not check what happens when the server is restarted between a write and a read (data loss), what happens when `skip` and `limit` are applied to a dictionary slice versus a MongoDB cursor, or what happens when two task-creation requests arrive simultaneously. These are not edge cases unique to tasks — they are the standard concerns for any storage layer — but they are only observable through the MongoDB-backed routes (milestones, progress) in the current test suite.

There is also no test for the token expiry behaviour: no test creates a token, waits for it to expire, and then confirms that the protected routes reject it. The 300-minute window makes this impractical to test without mocking the system clock.

---

## 6. Access and Security

### 6.1 User Roles

The system has two states for any incoming request: authenticated and unauthenticated. There are no role levels (no admin, no read-only, no project-owner distinctions) in the current implementation.

An **unauthenticated request** — one with no `Authorization` header, or a malformed token — receives an HTTP 401 response. The response body explains why the token was rejected. No record data is returned.

An **authenticated request** — one with a valid, non-expired Bearer token — can read, create, update, and delete any record in the system, regardless of which user created it. For example, an authenticated user who knows the MongoDB ObjectId of another user's milestone can delete it. The system does not check whether the requesting user owns the record being modified.

### 6.2 Login Security

**Password hashing with bcrypt.** When a user registers via `POST /users/`, the `create_user()` function in `app/models/user.py` calls `get_password_hash(password)` from `app/utils.py` before writing to MongoDB. This function uses passlib's `CryptContext` with the bcrypt scheme. bcrypt does not simply compute a hash of the input. It applies a cost factor — by default 12 in passlib — that causes the hash function to run 2¹² = 4,096 internal rounds. On a modern CPU this takes roughly 250 milliseconds per hash. An attacker checking one million password guesses per second against a plain SHA-256 hash could exhaust all 6-character lowercase passwords (26⁶ = 308,915,776 combinations) in about 5 minutes. Against bcrypt at cost factor 12, the same search would take approximately 21,000 hours, because each guess requires 250 ms rather than a fraction of a microsecond.

**Discrepancy in `auth.py`.** The `verify_password()` function defined in `app/routes/auth.py` (line 43) is:

```python
def verify_password(plain_password: str, hashed_password: str):
    return plain_password == hashed_password
```

This is a plain string comparison, not a bcrypt check. The correct bcrypt verification using passlib is already implemented in `app/utils.py`, but `auth.py` defines its own version and does not call the one in `utils.py`. The `authenticate_user()` function compares the incoming password against `HARD_CODED_PASSWORD` — a variable that is compared as plain text. This means the authentication path does not use bcrypt verification, even though user passwords are stored as bcrypt hashes. The hashing in `create_user()` and the verification in `authenticate_user()` are effectively disconnected.

**Token structure.** Tokens are signed with HS256 using a secret key read from the `SECRET_KEY` environment variable, defaulting to the string `"secret"` if the variable is not set. In a deployment where `SECRET_KEY` is not configured, any party who knows this default value can forge valid tokens.

---

## 7. Conclusion

The Project Management API v2 provides a working REST interface for creating and retrieving projects, milestones, tasks, and progress entries behind JWT authentication. The layered code structure keeps route logic and database logic separate, which makes individual components straightforward to read and modify in isolation.

The main structural gap is the split storage approach: milestones, users, and progress records are durable (written to MongoDB and confirmed before the response is sent), while task records are not (held in a Python dictionary that is emptied on every server restart). Because tasks are linked to both milestones and progress entries — a milestone holds a `task_id`, and progress entries track task completion — losing task records on restart breaks the relationships between the three resource types. Milestone and progress records that reference a task ID that no longer exists in `TASK_DATA` will return empty results from `GET /taskss/{id}` without any error, leaving the data in an inconsistent state.

The secondary gap is the disconnection between password hashing at registration and password verification at login. The system hashes passwords correctly when users are created, but the login path compares plain-text values and does not call the bcrypt verification function. Closing this gap requires updating `authenticate_user()` in `auth.py` to retrieve the user's stored hash from MongoDB and verify the incoming password against it using the `verify_password()` function already implemented in `utils.py`.

Both gaps are contained to specific files (`app/models/tasks.py` for storage, `app/routes/auth.py` for login verification) and can be addressed without changes to the route definitions or the Pydantic models.
