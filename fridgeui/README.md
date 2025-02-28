## Running the Frontend

### Option 1: Run Locally

1. Navigate to the frontend directory:
   ```sh
   cd fridgeui
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Enviroment Config (.env file)
This project uses `.env` file to store environment variobles,
after you clone the repo, please execute the commands below:
```bash
cp .env.example .env
```
modify .env file if necessary (replace any placeholder)

4. Start the React development server:
   ```sh
   npm start
   ```
   The frontend will be accessible at [http://localhost:3000](http://localhost:3000).

### Option 2: Run with Docker Compose

1. Clone the Repository:
   ```sh
   git clone <repository-url>
   cd <project-directory>
   ```
2. Build and Start the Frontend:
   ```sh
   docker-compose up --build frontend
   ```

## Stopping the Frontend
To stop the running frontend, press `Ctrl + C` or run:
```sh
docker-compose stop frontend
```

