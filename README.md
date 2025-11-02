# Website Content Search

## Description
This is a full-stack web application that allows users to search and retrieve website content.  
- **Backend:** Django + Django REST Framework  
- **Frontend:** React  
- Supports optional integration with a vector database for embedding-based searches.

---

## Prerequisites

### Backend
- Python 3.10 or higher
- Django 5.2.7
- Django REST Framework
- PostgreSQL (or any other supported database)
- (Optional) Vector database (e.g., Pinecone, Weaviate) if embedding search is used

### Frontend
- Node.js 18 or higher
- npm or yarn

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/vyshnaviar/Assignment.git
cd Assignment

### 2. Backend Setup
bash
Copy code
cd backend
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start backend server
python manage.py runserver
Backend runs on: http://localhost:8000

### 3. Frontend Setup
bash
Copy code
cd frontend

# Install dependencies
npm install

# Start frontend development server
npm start
Frontend runs on: http://localhost:3000


