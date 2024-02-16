import sqlite3


def connect_db():
    global conn
    conn = sqlite3.connect("database.db")
    print("Opened database successfully")


def create_all_table():
    conn.execute(
        """CREATE TABLE IF NOT EXISTS Users (
            firstName TEXT,
            lastName TEXT,
            EMP_ID TEXT,
            email TEXT,
            username TEXT,
            password TEXT,
            addr TEXT, 
            city TEXT, 
            pin TEXT, 
            isAdmin INTEGER DEFAULT 0)"""
    )

    conn.execute(
        """
    CREATE TABLE IF NOT EXISTS todo (
        TaskID	INTEGER,
	    UserName	TEXT,
	    Title	TEXT,
	    Description	TEXT,
	    Date	NUMERIC,
        Today INTEGER DEFAULT 0,
        Tommorow INTEGER DEFAULT 0,
	    Done	INTEGER DEFAULT 0,
	    Status	TEXT,
	    PRIMARY KEY("TaskID" AUTOINCREMENT)
     )"""
    )

    conn.execute(
        """CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            UserName Text, 
            name TEXT, 
            description TEXT)"""
    )

    conn.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            UserName TEXT, 
            TeamName TEXT,
            taskName TEXT, 
            taskDesc TEXT
            Today INTEGER DEFAULT 0,
            Tommorow INTEGER DEFAULT 0,
            Done	INTEGER DEFAULT 0,
	        Status	TEXT)"""
    )

    conn.execute(
        """CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            UserName TEXT, 
            teamName TEXT, 
            teamDesc TEXT, 
            teamMembers TEXT)"""
    )

    print("Table created successfully")


def close_db():
    conn.close()


connect_db()
create_all_table()
close_db()
