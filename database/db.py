import sqlite3

def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE NOT NULL,
                      email TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL,
                      country TEXT,
                      county TEXT,
                      profile_image TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS notifications (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_email TEXT NOT NULL,
                      message TEXT NOT NULL,
                      seen INTEGER DEFAULT 0,
                      street TEXT NOT NULL,
                      datetime DATETIME,
                      FOREIGN KEY (user_email) REFERENCES users(email))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS reports (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      description TEXT NOT NULL,
                      country TEXT NOT NULL,
                      county TEXT NOT NULL,
                      street TEXT NOT NULL,
                      datetime DATETIME)''')

    conn.commit()
    conn.close()
