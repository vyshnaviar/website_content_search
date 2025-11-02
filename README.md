******Website Content Search******
🧩 Description

Website Content Search is a full-stack web application that allows users to input a website URL and a search query to find the most relevant content chunks from that site.

It combines:

Frontend: React (modern UI for search and results display)

Backend: Django + Django REST Framework (handles HTML parsing, tokenization, and semantic similarity)

Optional Integration: Vector database (e.g., Milvus, Pinecone, or Weaviate) for embedding-based semantic search

⚙️ Prerequisites
🖥️ Backend

Python 3.10+

Django 5.2.7

Django REST Framework

PostgreSQL (or SQLite for local testing)

(Optional) Vector Database – Milvus, Pinecone, or Weaviate

💻 Frontend

Node.js 18+

npm or yarn

🚀 Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/vyshnaviar/Assignment.git
cd Assignment

2️⃣ Backend Setup
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the Django backend server
python manage.py runserver


Backend will be available at:
👉 http://localhost:8000

3️⃣ Frontend Setup
cd frontend

# Install dependencies
npm install

# Start the React frontend
npm start


Frontend will be available at:
👉 http://localhost:3000

4️⃣ Milvus Vector Database Setup (Optional but Recommended)

Milvus is used as a vector database to store and retrieve text embeddings for semantic search.

Prerequisites

Docker

Docker Compose

Install Docker

Install Docker Compose

Steps to Set Up Milvus

Navigate to your project root directory:

cd Assignment


Start Milvus with Docker Compose:

docker-compose up -d


Verify running containers:

docker-compose ps


You should see:

milvus-standalone – Milvus vector database

milvus-minio – Object storage

milvus-etcd – Metadata store

Check Milvus service logs:

docker-compose logs -f milvus-standalone


Wait for:

Milvus standalone ready to serve


Once running, the backend can connect automatically to perform semantic embedding searches.

🧠 Project Workflow

User enters:

Website URL

Search Query

Backend processes:

Fetches and cleans HTML content

Splits content into chunks

Tokenizes and embeds chunks

Stores/retrieves them in the vector database

Frontend displays:

Ranked list of relevant content chunks

Relevance score (e.g., 81.52% match)

Raw HTML snippet (optional)

🧰 Tech Stack
Layer	Technology
Frontend	React, HTML5, CSS3
Backend	Django, Django REST Framework
Database	PostgreSQL
Vector Database	Milvus (Docker-based)
Others	Fetch API, JSON, Python Embedding Models
📽️ Walkthrough Video (Recommended for Submission)

Create a short 5–10 minute demo video covering:

Application overview and purpose

Frontend walkthrough (search form and results view)

Query submission workflow

Backend explanation (HTML parsing, tokenization, similarity logic)

Vector database setup and connection

Codebase structure and file explanation

🧩 Challenges Faced

Handling inconsistent HTML structure from various websites

Achieving accurate tokenization for complex text

Balancing performance and relevance when embedding content

Managing CORS and cross-origin issues between backend and frontend

💡 Lessons Learned

Improved understanding of semantic search systems

Experience in full-stack integration with React and Django

Practical knowledge of vector databases for real-world text retrieval

🚀 Future Improvements

Add multi-language content support

Implement query caching and faster embedding storage

Integrate AI summarization of search results

Deploy project to cloud (AWS / Render / Vercel)

👩‍💻 Author

Vyshnavi A R
📧 vyshnaviar830@gmail.com
