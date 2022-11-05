import sqlite3 as sqlite3

connection =sqlite3.connect("hr.db")
print("Database Created Successfully")

connection.execute(""" CREATE TABLE RECRUITER (
    name TEXT,
    phone TEXT ,
    email TEXT NOT NULL UNIQUE,
    password TEXT, 
    id TEXT PRIMARY KEY,
    about_me TEXT,
    designation TEXT,
    experience TEXT,
    url TEXT,
    company_name TEXT,
    company_description TEXT,
    location TEXT,
    website TEXT,
    in_url TEXT )  """)

print("Table Recruiter Successfully")


connection.execute(""" CREATE TABLE OPENINGS (
    id TEXT,
    title TEXT,
    company_name TEXT,
    designation TEXT,
    salary_range TEXT,
    skills_required TEXT,
    roles_responsibilities TEXT,
    company_description TEXT,
    location TEXT,
    website TEXT,
    author TEXT NOT NULL )  """)

print("Table Openings successfully")

connection.close()