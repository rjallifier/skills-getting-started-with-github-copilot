# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities
- View participants and unregister them using the delete icon on each activity card

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/signup?email=student@mergington.edu` | Unregister a participant from an activity                            |

Unregistering returns a confirmation message. An unknown activity or a student
who is not registered returns HTTP 404. Participant lists and availability
refresh after successful signups and removals.

## Backend Tests

From the repository root, install the dependencies and run the pytest suite:

```sh
python -m pip install -r requirements.txt
python -m pytest -q
```

Tests live in [tests](../tests) and use FastAPI's `TestClient`, so no running
server is required. Every test follows Arrange-Act-Assert (AAA): prepare its
inputs, make the HTTP request, then verify the response and resulting state.
Shared fixtures provide isolated activity data for each test and restore the
application's original data afterward.

The suite covers activity retrieval, the root redirect, signup, duplicate
registration rejection, unregistering, missing email parameters, and registration
state integrity. Pytest discovery is also enabled in VS Code's Testing panel.

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
