from src.database import get_db_connection
from datetime import datetime

def create_notification(user_id, event_id, message, notif_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notifications (user_id, event_id, message, notification_type, created_at, read)
        VALUES (?, ?, ?, ?, ?, 0)
    """, (user_id, event_id, message, notif_type, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_user_notifications(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    notifs = cursor.fetchall()
    conn.close()
    return [dict(n) for n in notifs]
