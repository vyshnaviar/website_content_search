
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from pymilvus import connections, Collection, utility
# from sentence_transformers import SentenceTransformer
# from bs4 import BeautifulSoup
# from transformers import AutoTokenizer
# import requests
# import json
# import numpy as np
# import logging

# logger = logging.getLogger(__name__)

# # ---------------------------
# # 1. Connect to Milvus
# # ---------------------------
# try:
#     connections.connect("default", host="localhost", port="19530")
#     print("Connected to Milvus!")
# except Exception as e:
#     print(f" Milvus connection failed: {e}")
#     print(" Make sure Milvus is running on localhost:19530")

# # 2. Initialize Models

# model = SentenceTransformer("all-MiniLM-L6-v2")
# tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

# # 3. Helper functions

# def fetch_and_clean_html(url):
#     """Fetch HTML and clean it (remove scripts, styles, etc.)"""
#     try:
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#         }
#         r = requests.get(url, timeout=15, headers=headers)
#         r.raise_for_status()
        
#         soup = BeautifulSoup(r.text, "html.parser")
#         for tag in soup(["script", "style", "meta", "link", "noscript", "header", "footer", "nav"]):
#             tag.decompose()
        
#         text = soup.get_text(separator=" ", strip=True)
#         import re
#         text = re.sub(r'\s+', ' ', text).strip()
#         return text
#     except Exception as e:
#         logger.error(f"Failed to fetch URL {url}: {e}")
#         raise Exception(f"Failed to fetch URL: {str(e)}")

# def tokenize_and_chunk(text, max_tokens=500):
#     """Tokenize text and split into chunks of max_tokens (500)"""
#     tokens = tokenizer.encode(text, add_special_tokens=False)
#     chunk_texts = []
#     chunk_token_counts = []
    
#     for i in range(0, len(tokens), max_tokens):
#         chunk_tokens = tokens[i:i + max_tokens]
#         chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
#         if chunk_text.strip():
#             chunk_texts.append(chunk_text.strip())
#             chunk_token_counts.append(len(chunk_tokens))
    
#     return chunk_texts, chunk_token_counts

# def normalize_embeddings(embeddings):
#     """Normalize embeddings for cosine similarity search"""
#     arr = np.array(embeddings)
#     norm = np.linalg.norm(arr, axis=1, keepdims=True)
#     return (arr / (norm + 1e-10)).tolist()

# # 4. API: Add URL content

# @csrf_exempt
# def add_url(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             url = data.get("url")
#             if not url:
#                 return JsonResponse({"error": "URL is required"}, status=400)

#             text = fetch_and_clean_html(url)
#             if not text:
#                 return JsonResponse({"error": "Failed to fetch or clean HTML"}, status=400)

#             chunks, token_counts = tokenize_and_chunk(text, max_tokens=500)
#             embeddings = normalize_embeddings(model.encode(chunks))

#             collection_name = "html_chunks"
#             if collection_name not in utility.list_collections():
#                 from pymilvus import CollectionSchema, FieldSchema, DataType
#                 fields = [
#                     FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
#                     FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=500),
#                     FieldSchema(name="chunk", dtype=DataType.VARCHAR, max_length=5000),
#                     FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
#                 ]
#                 schema = CollectionSchema(fields, description="HTML content chunks")
#                 collection = Collection(name=collection_name, schema=schema)
#                 index_params = {"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 128}}
#                 collection.create_index("embedding", index_params)
#                 print(" Collection created with index")
#             else:
#                 collection = Collection(collection_name)
            
#             collection.load()
#             entities = [[url]*len(chunks), chunks, embeddings]
#             collection.insert(entities)
#             collection.flush()
            
#             return JsonResponse({"status": "success", "chunks_added": len(chunks), "url": url})

#         except Exception as e:
#             logger.error(f"Error in add_url: {e}", exc_info=True)
#             return JsonResponse({"error": str(e)}, status=500)
    
#     return JsonResponse({"error": "Invalid request method"}, status=400)

# # 5. API: Search HTML chunks

# # @csrf_exempt
# # @api_view(['POST'])
# # def search_html(request):
# #     if request.method == "POST":
# #         try:
# #             data = request.data if request.content_type=='application/json' else json.loads(request.body)
# #             url = data.get("url", "").strip()
# #             query = data.get("query", "").strip()
# #             print(query +"==="+ url)
# #             if not url:
# #                 return Response({'success': False, 'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)
# #             if not query:
# #                 return Response({'success': False, 'error': 'Search query is required'}, status=status.HTTP_400_BAD_REQUEST)
# #             if not url.startswith(('http://', 'https://')):
# #                 return Response({'success': False, 'error': 'URL must start with http:// or https://'}, status=status.HTTP_400_BAD_REQUEST)
            
# #             logger.info(f"Processing search - URL: {url}, Query: {query}")
# #             text = fetch_and_clean_html(url)
# #             chunks, token_counts = tokenize_and_chunk(text, max_tokens=500)
# #             if not chunks:
# #                 raise Exception("No chunks generated from content")

# #             embeddings = normalize_embeddings(model.encode(chunks))

# #             # ---------------------------
# #             # Compute cosine similarity for relevance %
# #             # ---------------------------
# #             query_emb = normalize_embeddings(model.encode([query]))[0]
# #             embeddings_np = np.array(embeddings)
# #             query_emb_np = np.array(query_emb)
# #             dot_products = np.dot(embeddings_np, query_emb_np)
# #             embeddings_norm = np.linalg.norm(embeddings_np, axis=1)
# #             query_norm = np.linalg.norm(query_emb_np)
# #             embeddings_norm[embeddings_norm == 0] = 1e-10
# #             if query_norm == 0:
# #                 query_norm = 1e-10
# #             cosine_scores = dot_products / (embeddings_norm * query_norm)
# #             cosine_scores = np.clip(cosine_scores, 0.0, 1.0)

# #             top_indices = np.argsort(-cosine_scores)[:10]
# #             matched_chunks = []
# #             for rank, idx in enumerate(top_indices, start=1):
# #                 matched_chunks.append({
# #                     "rank": rank,
# #                     "content": chunks[idx],
# #                     "relevance_score": round(float(cosine_scores[idx]*100), 1),  # percentage
# #                     "token_count": token_counts[idx]
# #                 })

# #             return Response({'success': True, 'url': url, 'query': query, 'total_results': len(matched_chunks), 'results': matched_chunks}, status=status.HTTP_200_OK)

# #         except Exception as e:
# #             logger.error(f"Search failed: {str(e)}", exc_info=True)
# #             return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# #     return Response({'error': 'Invalid request method'}, status=400)
# @csrf_exempt
# @api_view(['POST'])
# def search_html(request):
#     """
#     Semantic search endpoint
#     Accepts URL and query, returns top 10 matches
#     """
#     try:
#         # Accept both JSON body and query parameters
#         url = request.data.get("url") or request.GET.get("url")
#         query = request.data.get("query") or request.GET.get("query")

#         if not url:
#             return Response({'success': False, 'error': 'URL is required'}, status=400)
#         if not query:
#             return Response({'success': False, 'error': 'Query is required'}, status=400)
#         if not url.startswith(('http://', 'https://')):
#             return Response({'success': False, 'error': 'URL must start with http:// or https://'}, status=400)

#         logger.info(f"Processing search - URL: {url}, Query: {query}")

#         # Fetch and clean HTML
#         text = fetch_and_clean_html(url)

#         # Tokenize and chunk
#         chunks, token_counts = tokenize_and_chunk(text, max_tokens=500)

#         # Generate embeddings
#         embeddings = normalize_embeddings(model.encode(chunks))

#         # Setup Milvus temporary collection
#         collection_name = "html_chunks_temp"
#         if collection_name in utility.list_collections():
#             utility.drop_collection(collection_name)

#         from pymilvus import CollectionSchema, FieldSchema, DataType
#         fields = [
#             FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
#             FieldSchema(name="chunk", dtype=DataType.VARCHAR, max_length=5000),
#             FieldSchema(name="token_count", dtype=DataType.INT64),
#             FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
#         ]
#         schema = CollectionSchema(fields, description="Temporary search chunks")
#         collection = Collection(name=collection_name, schema=schema)

#         # Create index
#         index_params = {"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 128}}
#         collection.create_index("embedding", index_params)

#         # Insert chunks
#         collection.insert([chunks, token_counts, embeddings])
#         collection.flush()
#         collection.load()

#         # Search
#         query_emb = normalize_embeddings(model.encode([query]))
#         search_params = {"metric_type": "COSINE", "params": {"nprobe": 20}}
#         top_k = min(10, len(chunks))

#         results = collection.search(
#             data=query_emb,
#             anns_field="embedding",
#             param=search_params,
#             limit=top_k,
#             output_fields=["chunk", "token_count"]
#         )

#         matched_chunks = []
#         for i, hit in enumerate(results[0]):
#             # Convert cosine distance to similarity %
#             relevance_pct = round((1 - float(hit.distance)) * 100, 2)
#             matched_chunks.append({
#                 'rank': i + 1,
#                 'content': hit.entity.get("chunk"),
#                 'relevance_score': relevance_pct,
#                 'token_count': hit.entity.get("token_count"),
#             })

#         return Response({
#             'success': True,
#             'url': url,
#             'query': query,
#             'total_results': len(matched_chunks),
#             'results': matched_chunks
#         }, status=200)

#     except Exception as e:
#         logger.error(f"Search failed: {str(e)}", exc_info=True)
#         return Response({'success': False, 'error': str(e)}, status=500)

# # 6. Health Check

# @api_view(['GET'])
# def health_check(request):
#     try:
#         collections = utility.list_collections()
#         return Response({'status': 'healthy', 'message': 'Semantic Search API is running', 'milvus_connected': True, 'collections': len(collections)}, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({'status': 'unhealthy', 'message': str(e), 'milvus_connected': False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pymilvus import connections, Collection, utility
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup
from transformers import AutoTokenizer
import requests
import json
import numpy as np
import logging

logger = logging.getLogger(__name__)

# ---------------------------
# 1. Connect to Milvus
# ---------------------------
try:
    connections.connect("default", host="localhost", port="19530")
    print("Connected to Milvus!")
except Exception as e:
    print(f"Milvus connection failed: {e}")
    print("Make sure Milvus is running on localhost:19530")

# 2. Initialize Models
model = SentenceTransformer("all-MiniLM-L6-v2")
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

# ---------------------------
# 3. Helper functions
# ---------------------------
MAX_HTML_CHUNK_LENGTH = 3000  # max length for DOM element in Milvus

def fetch_html_dom_chunks(url, max_length=MAX_HTML_CHUNK_LENGTH):
    """
    Fetch HTML content and return a list of HTML DOM elements
    Each chunk is truncated to max_length to avoid Milvus VARCHAR errors
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        r = requests.get(url, timeout=15, headers=headers)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        # Remove unwanted tags
        for tag in soup(["script", "style", "meta", "link", "noscript", "header", "footer", "nav"]):
            tag.decompose()

        html_chunks = []
        # Extract block-level elements
        for element in soup.find_all(["p", "div", "section", "article", "span", "li"]):
            html_str = str(element)
            if len(html_str) > max_length:
                html_str = html_str[:max_length]
            html_chunks.append(html_str)

        # Full cleaned text for embedding
        text = soup.get_text(separator=" ", strip=True)
        import re
        text = re.sub(r'\s+', ' ', text).strip()
        return text, html_chunks
    except Exception as e:
        logger.error(f"Failed to fetch URL {url}: {e}")
        raise Exception(f"Failed to fetch URL: {str(e)}")


def tokenize_and_chunk(text, max_tokens=500):
    """Tokenize text and split into chunks"""
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunk_texts = []
    chunk_token_counts = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        if chunk_text.strip():
            chunk_texts.append(chunk_text.strip())
            chunk_token_counts.append(len(chunk_tokens))
    return chunk_texts, chunk_token_counts

def normalize_embeddings(embeddings):
    """Normalize embeddings for cosine similarity"""
    arr = np.array(embeddings)
    norm = np.linalg.norm(arr, axis=1, keepdims=True)
    return (arr / (norm + 1e-10)).tolist()


# ---------------------------
# 4. API: Add URL content
# ---------------------------
@csrf_exempt
def add_url(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            url = data.get("url")
            if not url:
                return JsonResponse({"error": "URL is required"}, status=400)

            text, html_chunks = fetch_html_dom_chunks(url)
            chunks, token_counts = tokenize_and_chunk(text, max_tokens=500)
            embeddings = normalize_embeddings(model.encode(chunks))

            # Truncate html_chunks to match chunks
            html_chunks = html_chunks[:len(chunks)]

            collection_name = "html_chunks"
            if collection_name not in utility.list_collections():
                from pymilvus import CollectionSchema, FieldSchema, DataType
                fields = [
                    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                    FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=500),
                    FieldSchema(name="chunk", dtype=DataType.VARCHAR, max_length=5000),
                    FieldSchema(name="html_chunk", dtype=DataType.VARCHAR, max_length=MAX_HTML_CHUNK_LENGTH),
                    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
                ]
                schema = CollectionSchema(fields, description="HTML content chunks")
                collection = Collection(name=collection_name, schema=schema)
                index_params = {"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 128}}
                collection.create_index("embedding", index_params)
                print("Collection created with index")
            else:
                collection = Collection(collection_name)

            collection.load()
            entities = [[url]*len(chunks), chunks, html_chunks, embeddings]
            collection.insert(entities)
            collection.flush()

            return JsonResponse({"status": "success", "chunks_added": len(chunks), "url": url})

        except Exception as e:
            logger.error(f"Error in add_url: {e}", exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)


# ---------------------------
# 5. API: Search HTML chunks
# ---------------------------
@csrf_exempt
@api_view(['POST'])
def search_html(request):
    try:
        url = request.data.get("url") or request.GET.get("url")
        query = request.data.get("query") or request.GET.get("query")

        if not url:
            return Response({'success': False, 'error': 'URL is required'}, status=400)
        if not query:
            return Response({'success': False, 'error': 'Query is required'}, status=400)
        if not url.startswith(('http://', 'https://')):
            return Response({'success': False, 'error': 'URL must start with http:// or https://'}, status=400)

        logger.info(f"Processing search - URL: {url}, Query: {query}")

        # Fetch HTML DOM elements
        text, html_chunks = fetch_html_dom_chunks(url)
        chunks, token_counts = tokenize_and_chunk(text, max_tokens=500)

        # Align HTML chunks with token chunks
        html_chunks = html_chunks[:len(chunks)]

        # Generate embeddings
        embeddings = normalize_embeddings(model.encode(chunks))

        # Temporary Milvus collection for search
        collection_name = "html_chunks_temp"
        if collection_name in utility.list_collections():
            utility.drop_collection(collection_name)

        from pymilvus import CollectionSchema, FieldSchema, DataType
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="chunk", dtype=DataType.VARCHAR, max_length=5000),
            FieldSchema(name="html_chunk", dtype=DataType.VARCHAR, max_length=MAX_HTML_CHUNK_LENGTH),
            FieldSchema(name="token_count", dtype=DataType.INT64),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
        ]
        schema = CollectionSchema(fields, description="Temporary search chunks")
        collection = Collection(name=collection_name, schema=schema)

        # Create index
        index_params = {"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 128}}
        collection.create_index("embedding", index_params)

        # Insert chunks
        collection.insert([chunks, html_chunks, token_counts, embeddings])
        collection.flush()
        collection.load()

        # Search
        query_emb = normalize_embeddings(model.encode([query]))
        search_params = {"metric_type": "COSINE", "params": {"nprobe": 20}}
        top_k = min(10, len(chunks))

        results = collection.search(
            data=query_emb,
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["chunk", "html_chunk", "token_count"]
        )

        # matched_chunks = []
        # for i, hit in enumerate(results[0]):
        #     similarity = max(0.0, 1.0 - hit.distance)  # convert distance to similarity
        #     matched_chunks.append({
        #         'rank': i + 1,
        #         'content': hit.entity.get("chunk"),
        #         'html_chunk': hit.entity.get("html_chunk"),  # return actual DOM element
        #         'relevance_score': round(similarity * 100, 2),  # proper percentage
        #         'token_count': hit.entity.get("token_count"),
        #     })
        matched_chunks = []
        for i, hit in enumerate(results[0]):
        # Convert distance to similarity
            similarity = 1.0 - hit.distance
            similarity = min(max(similarity, 0.0), 1.0)  # clamp between 0 and 1
            matched_chunks.append({
                'rank': i + 1,
                'content': hit.entity.get("chunk"),
                'html_chunk': hit.entity.get("html_chunk"),
                'relevance_score': round(similarity * 100, 2),  # proper percentage
                'token_count': hit.entity.get("token_count"),
            })

        return Response({
            'success': True,
            'url': url,
            'query': query,
            'total_results': len(matched_chunks),
            'results': matched_chunks
        }, status=200)

    except Exception as e:
        logger.error(f"Search failed: {str(e)}", exc_info=True)
        return Response({'success': False, 'error': str(e)}, status=500)


# ---------------------------
# 6. Health Check
# ---------------------------
@api_view(['GET'])
def health_check(request):
    try:
        collections = utility.list_collections()
        return Response({
            'status': 'healthy',
            'message': 'Semantic Search API is running',
            'milvus_connected': True,
            'collections': len(collections)
        }, status=200)
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'message': str(e),
            'milvus_connected': False
        }, status=503)
