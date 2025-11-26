# ScriptExecuterServer

ScriptExecuterServer is a lightweight, containerized application designed to dynamically execute and manage Python scripts via a simple web interface and a RESTful API. It allows users to upload and run custom scripts with separate trigger and main logic, which are then executed periodically by a background scheduler.

## Current Features

*   **RESTful API**: Endpoints to add, view, and delete scripts.
*   **Dynamic Script Execution**: Upload custom Python scripts at runtime.
*   **Scheduled Execution**: A background runner executes scripts at defined intervals.
*   **Simple Web Dashboard**: A basic frontend to upload new scripts and view currently active ones.
*   **Containerized**: Separate Dockerfiles for the FastAPI backend and the static frontend, making it easy to deploy.

## Roadmap

This project is in its early stages. Here is a roadmap of planned features and improvements to enhance its functionality, security, and user experience.

### 1. Persistent Storage

Currently, all active scripts are stored in-memory, meaning they are lost when the server restarts. The highest priority is to implement a persistent storage solution.

*   **Database Integration**: Use a database like **SQLite** for simplicity or **PostgreSQL** for more robust needs to store script metadata, code, and execution history.
*   **File-Based Storage**: Alternatively, store script configurations in a structured way on the file system (e.g., using JSON or YAML files) to persist state between restarts.

### 2. Authentication & Security

To protect the API and control access, a proper authentication mechanism is necessary.

*   **API Key Authentication**: Implement a simple API key system for backend services.
*   **User Accounts & JWT**: For a multi-user environment, introduce user accounts with JWT-based authentication for the dashboard.
*   **Role-Based Access Control (RBAC)**: Define roles (e.g., admin, user) to restrict permissions for certain actions like adding or deleting scripts.

### 3. Enhanced Dashboard

The current dashboard is very basic. The goal is to create a more powerful and interactive user interface.

*   **View Script Details**: Allow users to view the code, execution status, and output/logs of each script directly in the dashboard.
*   **In-Browser Editor**: Integrate a code editor (like Monaco or CodeMirror) to allow creating and editing scripts without needing to upload files.
*   **Manual Trigger & Deactivation**: Add buttons to manually trigger a script's execution or temporarily deactivate it.
*   **Real-time Updates**: Use WebSockets to provide real-time updates on script status and logs.

### 4. Custom Module Installation

Scripts are currently limited to the Python standard library and modules installed in the base Docker image. A key feature will be allowing scripts to have their own dependencies.

*   **Virtual Environments**: Isolate each script in its own virtual environment to manage dependencies without conflicts.
*   **`requirements.txt` per Script**: Allow users to upload a `requirements.txt` file along with their script, which the server will use to install the necessary packages.
*   **Dynamic Module Installation**: Implement a mechanism to securely install packages on-the-fly when a new script is added.

## Getting Started

The application is split into two services: a backend API and a frontend client.

### Prerequisites

*   Docker

### Running the Services

1.  **Build and run the API:**
    ```shell
    docker build -t script-api src/api
    docker run -d -p 8000:8000 --name api-container script-api
    ```

2.  **Build and run the Client:**
    ```shell
    docker build -t script-client src/client
    docker run -d -p 8080:80 --name client-container script-client
    ```

You can now access the dashboard at `http://localhost:8080`.
