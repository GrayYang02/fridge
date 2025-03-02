# Backend Setup

This document provides instructions for setting up and running the Django backend.

## Prerequisites

Ensure you have the following installed:

- [Python & pip](https://www.python.org/)
- [Docker](https://www.docker.com/get-started) (if using Docker Compose)

## Running the Backend

### Option 1: Run Locally

1. Navigate to the backend directory:
   ```sh
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv ~/env/venv
   source ~/env/venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the Django server:
   ```sh
   python manage.py runserver
   ```
   The backend will be accessible at [http://localhost:8000](http://localhost:8000).

5. Run the test_views.py for tests of views:
   python manage.py test core     

### Option 2: Run with Docker Compose

1. Clone the Repository:
   ```sh
   git clone <repository-url>
   cd <project-directory>
   ```
2. Build and Start the Backend:
   ```sh
   docker-compose up --build backend
   ```

## Stopping the Backend
To stop the running backend, press `Ctrl + C` or run:
```sh
docker-compose stop backend
```

# DataBase Setup
If show: 
`django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module.
Did you install mysqlclient?`

and do
###### pip install mysqlclient
still do not working

### FIX!
do
```aiignore
brew install pkg-config
brew install mariadb
brew link mariadb
pip install mysqlclient
```

# Frontend Setup

This document provides instructions for setting up and running the React frontend.

## Prerequisites

Ensure you have the following installed:

- [Node.js](https://nodejs.org/)
- [Docker](https://www.docker.com/get-started) (if using Docker Compose)

