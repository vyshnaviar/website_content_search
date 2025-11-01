from django.urls import path
from .views import add_url, search_html, health_check

urlpatterns = [
    # Health check endpoint
    path('health/', health_check, name='health_check'),
    
    # Assignment endpoint: Semantic search (URL + query)
    path('search/', search_html, name='search_html'),
    
    # Your existing endpoint: Add URL to collection
    path('add-url/', add_url, name='add_url'),
]
