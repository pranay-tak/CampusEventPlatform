import json
from src.database import get_db_connection

def get_recommendations(user_id):
    """
    Simple Content-based Recommendation System.
    Scores events based on user interests vs event tags/category.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get User Interests
    cursor.execute("SELECT interests FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        return []
    
    user_interests = json.loads(row['interests']) if row['interests'] else []
    
    # Get all upcoming events
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    
    recommendations = []
    for event in events:
        score = 0
        tags = json.loads(event['tags']) if event['tags'] else []
        category = event['category']
        
        # Scoring logic
        if category in user_interests:
            score += 40
            
        for interest in user_interests:
            if interest in tags:
                score += 25
                
        # Simulate past interaction score
        cursor.execute("SELECT COUNT(*) FROM interactions WHERE user_id = ? AND event_id = ?", (user_id, event['id']))
        interaction_count = cursor.fetchone()[0]
        if interaction_count > 0:
            score += 20
            
        if score > 0:
            recommendations.append({
                "event": dict(event),
                "score": score,
                "reason": f"Recommended because it matches your interests in {', '.join(user_interests)}"
            })
            
    conn.close()
    
    # Sort by score descending
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return recommendations
