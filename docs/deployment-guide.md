# Deployment Guide

## 1. Requirements

Before deploying the Warranty Request Classification System, ensure that the following requirements are met:

- **Operating System:** Windows 10/11, Linux, or macOS.
- **Docker:** Docker Desktop or Docker Engine.
- **Docker Compose:** Docker Compose V2.
- **Git:** Required to clone the project repository.
- **Available Disk Space:** At least 2 GB of free space is recommended.
- **Network:** Internet access is required during the initial Docker image build to install Python dependencies.
- **Port:** Port `8501` must be available on the host machine by default.

No local Python installation, Node.js, or external database server is required to run the application.

## 2. Setup Steps

### Step 1: Clone the repository

```bash
git clone --branch v1.0 https://github.com/npt8124/cdtn1-nguyenphuocthanh-l10
```

### Step 2: Navigate to the project directory

```bash
cd cdtn1-nguyenphuocthanh-l10
```

### Step 3: Create the environment file

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

On Linux or macOS:

```bash
cp .env.example .env
```

The default configuration uses port `8501`.

### Step 4: Build and start the application

Run the following command:

```bash
docker compose up -d --build
```

During the image build process, Docker will:

1. Install the required Python dependencies.
2. Copy the application source code and training dataset.
3. Train the machine learning model using `configs/train.yaml`.
4. Generate `artifacts/warranty_model.joblib`.
5. Generate `reports/metrics.json`.
6. Start the Streamlit application.

The first build may take several minutes depending on the network connection and machine performance.

### Step 5: Access the application

Open the following address in a web browser:

```text
http://localhost:8501
```

The Warranty Request Classification System should now be available.

## 3. Environment Variables

The application uses the following environment variable for deployment:

| Variable | Meaning | Sample | Required |
|---|---|---|---|
| `APP_PORT` | Host port mapped to the application's internal port 8501 | `8501` | No |

If `APP_PORT` is not specified, Docker Compose uses `8501` by default.

For example, to access the application through port `8080`, update `.env`:

```env
APP_PORT=8080
```

Then access:

```text
http://localhost:8080
```

## 4. Sample Data

The project uses two different types of data:

### Machine Learning Dataset

The training dataset is located at:

```text
src/data/mau/issue_descriptions.csv
```

It contains warranty issue descriptions and their corresponding categories.

During the Docker image build, the training process reads this dataset and generates the trained model:

```text
artifacts/warranty_model.joblib
```

Evaluation results are generated at:

```text
reports/metrics.json
```

No separate model training command is required after deployment.

### Application Database

The application uses SQLite to store confirmed warranty requests and their modification history.

The database file is:

```text
data/warranty.sqlite3
```

Docker Compose mounts a persistent named volume at `/app/data` inside the container. This ensures that application records remain available when the container is restarted or recreated.

The database tables are initialized automatically when the application starts.

The database does not contain preloaded warranty request records. New records are created when users classify and confirm warranty requests through the application.

## 5. Verify It Works

### Step 1: Check the container status

```bash
docker compose ps
```

Expected result:

- The `warranty-classifier` container is running.
- Port `8501` is published.
- The health status becomes `healthy` after the application starts successfully.

### Step 2: Check the application health endpoint

On Linux or macOS:

```bash
curl http://localhost:8501/_stcore/health
```

On Windows PowerShell:

```powershell
Invoke-WebRequest http://localhost:8501/_stcore/health
```

Expected response:

```text
ok
```

### Step 3: Run the automated tests

Execute the existing test suite inside the container:

```bash
docker compose exec app python -m pytest -q
```

Expected result if all tests pass:

```text
11 passed
```

The actual output may differ if the test suite changes.

### Step 4: View application logs

```bash
docker compose logs -f app
```

This command displays the application's runtime logs. Press `Ctrl + C` to stop following the logs.

### Step 5: Stop the application

```bash
docker compose down
```

This stops and removes the container while preserving the named database volume.

**Important:** To remove the database volume and all stored application records, use:

```bash
docker compose down -v
```

This operation permanently deletes the persisted SQLite data. Do not use it when you need to retain warranty request records.
