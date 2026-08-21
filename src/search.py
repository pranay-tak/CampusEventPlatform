from src.llm import generate_text
from src.database import get_db_connection
import json

def process_natural_language_search(query):
    """
    Uses Local LLM to convert a natural language query into search filters.
    """
    system_prompt = """
    You are a search assistant for a university events platform.
    Convert the user's natural language query into a JSON object with search filters.
    Possible keys: 'category' (string), 'time_period' (string like 'today', 'weekend', 'week'), 'keyword' (string).
    Only return valid JSON. Do not invent data.
    """
    
    prompt = f"Query: '{query}'\nReturn JSON filters."
    response = generate_text(prompt, system_prompt=system_prompt)
    
    try:
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0].strip()
        else:
            json_str = response.strip()
            
        filters = json.loads(json_str)
        return perform_db_search(filters)
    except:
        # Fallback to basic keyword search if LLM parsing fails
        return perform_db_search({"keyword": query})

def perform_db_search(filters):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM events WHERE 1=1"
    params = []
    
    if "category" in filters and filters["category"]:
        query += " AND category LIKE ?"
        params.append(f"%{filters['category']}%")
        
    if "keyword" in filters and filters["keyword"]:
        query += " AND (title LIKE ? OR description LIKE ? OR tags LIKE ?)"
        params.extend([f"%{filters['keyword']}%", f"%{filters['keyword']}%", f"%{filters['keyword']}%"])
        
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]
