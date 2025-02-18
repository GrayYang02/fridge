# Project Setup

This project consists of a frontend built with React and a backend powered by Django. The services are managed using Docker Compose.

## Prerequisites

Ensure you have the following installed on your system:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

### 1. Clone the Repository
```sh
git clone <repository-url>
cd <project-directory>
```

### 2. Build and Start the Services
Run the following command to build and start the containers:
```sh
docker-compose up --build
```
This will:
- Build and start the Django backend on port `8000`
- Build and start the React frontend on port `3000`

### 3. Access the Application
Once the services are running, you can access:
- **Frontend:** [http://localhost:3000](http://localhost:3000)
- **Backend:** [http://localhost:8000](http://localhost:8000)

## Stopping the Services
To stop the running containers, press `Ctrl + C` or run:
```sh
docker-compose down
```

## File Structure
```
.
├── backend/             # Django backend source code
│   ├── Dockerfile.django  # Dockerfile for backend service
│   └── ...
├── fridgeui/           # React frontend source code
│   ├── Dockerfile.react   # Dockerfile for frontend service
│   └── ...
├── docker-compose.yml  # Docker Compose configuration
└── README.md           # Project documentation
```

## Notes
- Ensure all dependencies for both frontend and backend are correctly installed within their respective containers.
- Modify `docker-compose.yml` if you need to change ports or configurations.

## Troubleshooting
- If a service fails to start, check logs using:
  ```sh
  docker-compose logs
  ```
- To rebuild services without using cache:
  ```sh
  docker-compose build --no-cache
  ```

