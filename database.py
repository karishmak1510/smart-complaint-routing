import sqlite3

# Connect database
conn = sqlite3.connect(
    "complaints.db",
    check_same_thread=False
)

cursor = conn.cursor()

# Users table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT UNIQUE

    )
    '''
)

# Complaints table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS complaints (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_email TEXT,

        complaint TEXT,

        department TEXT,

        status TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    '''
)

conn.commit()