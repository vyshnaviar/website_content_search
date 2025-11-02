Website Content Semantic Search

A full-stack web application to fetch website content, split into chunks, and perform semantic search using a vector database (Milvus). Users can input a URL and a search query to retrieve the most relevant chunks of content from the website.

Table of Contents

Project Overview

Features

Prerequisites

Backend Setup

Frontend Setup

Milvus Vector Database Setup

Running the Application

Additional Notes

Project Overview

This project allows users to:

Input a website URL.

Fetch HTML content and split it into manageable chunks.

Encode chunks using a SentenceTransformer model for semantic embeddings.

Store embeddings in Milvus vector database.

Perform semantic search to retrieve content most relevant to a user query.

Display results with content, relevance score, token count, and raw HTML DOM.

Features

Semantic search powered by sentence-transformers embeddings.

Tokenization and chunking of large website content.

Vector storage and search with Milvus v2.6.4.

React frontend with clean UI and interactive input boxes.

Relevance scores in percentage format.

HTML DOM display for deeper insights into website structure.

Prerequisites

Docker & Docker Compose: Install Docker

Python 3.10+

Node.js & npm or Yarn

Git

Internet connection (for fetching website data and installing packages)

Backend Setup

Navigate to the backend directory:

cd backend


Create and activate a Python virtual environment:

python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Run the Django development server:

python manage.py runserver


Backend API endpoints:

POST /api/add-url/ – Add website URL to database.

POST /api/search/ – Search for a query in a website’s content.

GET /api/health/ – Check API and Milvus status.

Frontend Setup

Navigate to the frontend directory:

cd frontend


Install dependencies:

npm install
# or
yarn install


Start the React development server:

npm start
# or
yarn start


Frontend URL: http://localhost:3000

Milvus Vector Database Setup

Ensure Docker and Docker Compose are installed.

Navigate to your project root containing docker-compose.yml.

Start Milvus with Docker Compose:

docker-compose up -d


Check running containers:

docker-compose ps


Expected services:

milvus-standalone – Milvus vector database.

milvus-minio – Object storage.

milvus-etcd – Metadata store.

Health check:

docker-compose logs -f milvus-standalone

Running the Application

Start Milvus (vector database):

docker-compose up -d


Start backend:

cd backend
venv\Scripts\activate  # Activate virtual environment
python manage.py runserver


Start frontend:

cd frontend
npm start


Open browser at http://localhost:3000 and start searching websites!

Additional Notes

Ensure Milvus is running before using the backend API.

Relevance scores are displayed as percentages (0–100%) for easier interpretation.

Maximum HTML chunk length and token chunk size can be configured in views.py.

Use a stable internet connection to fetch website content.

Use Ctrl + C in the terminal to stop backend or Milvus services.

Docker cleanup:
