# healthcare_management



# Project Setup Instructions

This project is a multi-layered web server architecture based on **Edge Computing** principles. It includes **Edge Nodes**, a **Central Node Server**, and a **Cloud Server**. Each server runs a **Django** web application, all containerized using **Docker**.

---

## Project Overview

- **Edge Node Servers**: Collect and manage data from IoT devices, wearables, and other edge devices.
- **Central Node Server**: Receives data from edge nodes, processes (anonymizes) it, and forwards it to the cloud server.
- **Cloud Server**: Stores the anonymized data received from the central node server and provides further processing capabilities.

---

## Prerequisites

Before you can set up the project, ensure you have the following installed:

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Project Structure

The project consists of three main components:

1. **Edge Node Server** (`Dockerfile.edge`):
   - Manages CRUD operations for data collection (e.g., patient data).
   
2. **Central Node Server** (`Dockerfile.central`):
   - Receives and anonymizes data from edge nodes, then sends it to the cloud.
   
3. **Cloud Server** (`Dockerfile.cloud`):
   - Receives anonymized data and performs centralized data storage.

Each server is a **Django** web app containerized using **Docker**.

---

## Setup Instructions

Follow these instructions to build and run the entire project.

### Step 1: Clone the Repository

First, clone this repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>



```markdown
cd path/to/your/projects

# Set up a virtual environment for the Edge Node Server
python -m venv edge_node_env
source edge_node_env/bin/activate

# Install Django and other dependencies
pip install django

# Create a requirements.txt file with the necessary dependencies
echo "Django>=3.2,<4" > requirements.txt
echo "djangorestframework>=3.12,<4" >> requirements.txt

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Create a new Django project for the Cloud Server
django-admin startproject cloud_server
cd cloud_server

# Start a new Django app for data collection
python manage.py startapp data_collection
```



List of Virtual Env Required 

python -m venv edge_node_env
source edge_node_env/bin/activate

python -m venv cloud_server_env
source cloud_server_env/bin/activate

python -m venv central_edge_node_env
source central_edge_node_env/bin/activate