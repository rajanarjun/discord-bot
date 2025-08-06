import sqlite3
from datetime import datetime

conn = sqlite3.connect("db/status.db")
cur = conn.cursor()

def create_status_table():
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS status (
                username TEXT,
                status TEXT,
                time TEXT
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")


def update_status(username, status):
    cur_time = datetime.now()
    cur_time_str = cur_time.strftime("%Y-%m-%d %H:%M:%S")  
    try:
        cur.execute("""
            INSERT INTO status (username, status, time) 
            VALUES (?, ?, ?)
            """, (username, status, cur_time_str))
        conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")


def how_long_ago(status_ts):
    now = datetime.now()
    status_ts_format = "%Y-%m-%d %H:%M:%S"
    saved_time = datetime.strptime(status_ts, status_ts_format)
    diff = now - saved_time
    if diff.seconds <= 3600:
        if diff.seconds <= 60:
            if diff.seconds <= 5:
                return f"Just now"
            else:
                return f"{diff.seconds} seconds ago"
        else:
            minutes = diff.seconds // 60
            if minutes == 1:
                return f"{minutes} minute ago"
            else:
                return f"{minutes} minutes ago"
    else:
        hours = diff.seconds // 3600
        if hours == 1:
            return f"{hours} hour ago"
        else:
            return f"{hours} hours ago"


def get_user_status():
    pass


def get_all_status():
    try:
        cur.execute("SELECT * FROM status")
        rows = cur.fetchall()
        lines = ["Currently Studying: "]
        for row in rows:
            t = how_long_ago(row[2])
            s = f"* {row[0]} — {row[1]} ({t})" 
            lines.append(s)
        result = "\n".join(lines)
        return result

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return "Sorry! Cant fetch status currently."

def close_status_db():
    if conn:
        conn.close()

if __name__ == "__main__":
    create_status_table()
    update_status('arjun', 'project')
    update_status('ravi', 'dsa')
    result = get_all_status()
    print(result)
