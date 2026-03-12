import sqlite3

def get_connection():
    conn = sqlite3.connect("jobs.db")
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            date_applied TEXT NOT NULL,
            notes TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database ready!")

def add_job(company, role, status, date_applied, notes=""):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO jobs (company, role, status, date_applied, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (company, role, status, date_applied, notes))
    
    conn.commit()
    conn.close()

def get_all_jobs():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    
    conn.close()
    return jobs

if __name__ == "__main__":
    create_table()
    add_job("Google", "Data Analyst", "Applied", "2025-03-12", "Found on LinkedIn")
    jobs = get_all_jobs()
    for job in jobs:
        print(job)
