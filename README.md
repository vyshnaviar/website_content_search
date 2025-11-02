# Website Content Search

## Description
This project is a full-stack web application that allows users to search and retrieve website content.  
- **Backend:** Django + Django REST Framework  
- **Frontend:** React  
- **Vector Database:** Milvus (optional, for embedding-based search)

---

## Prerequisites

### Backend
- Python 3.10 or higher
- Django 5.2.7
- Django REST Framework
- PostgreSQL (or another supported database)

### Frontend
- Node.js 18 or higher
- npm or yarn

### Vector Database (Optional)
- Docker
- Milvus (for embedding-based searches)

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/vyshnaviar/Assignment.git
cd Assignment

### 2. Backend Setup
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the backend server
python manage.py runserver
Backend runs on: http://localhost:8000
3. Frontend Setup
cd frontend

# Install dependencies
npm install

# Start the frontend development server
npm start

Frontend runs on: http://localhost:3000

## install milvus inside docker
Step 1: Make sure Docker Desktop is running

Open Docker Desktop → check “Docker Engine is running”
In Command Prompt, verify:

docker --version
docker ps

If these work, Docker is ready 
#Install Milvus Python client in backend environment:

pip install pymilvus


