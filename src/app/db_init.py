'''
CS3250 - Software Development Methods and Tools - Final Project
Module Name: db_init.py
Description: Database and Database Tables Initialization
Authors: Yedani Mendoza Gurrola, Artem Marsh, Jose Gomez Betancourt, Alexander Gonzalez Ramirez, Rhodes Ferris
'''

import psycopg2
import os
from psycopg2 import sql

DATABASE_USER = "postgres"
DATABASE_USER_PWD = "postgres1234"
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"

POSTGRESQL_DB = 'postgres'
BUDGETING_DB = 'budgeting'

connection = None
cursor = None

def Initialize_Database():
    try:
        connection = psycopg2.connect(
            user=DATABASE_USER,
            password=DATABASE_USER_PWD,
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database=POSTGRESQL_DB
        )
        connection.autocommit = True
        cursor = connection.cursor()
        
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'budgeting';")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(sql.SQL('CREATE DATABASE {};').format(sql.Identifier(BUDGETING_DB)))
            print(f"Created new database: {BUDGETING_DB}")

        connection.commit()
        print(f"Initialized database object")
    except Exception as error:
        print(f"An error occurred with initializing the database: {error}")
    finally:
        if cursor is not None: cursor.close()
        if connection is not None: connection.close()

def Initialize_Tables():
    try:
        connection = psycopg2.connect(
            user=DATABASE_USER,
            password=DATABASE_USER_PWD,
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database=BUDGETING_DB
        )
        connection.autocommit = True
        cursor = connection.cursor()

        schema_path = os.path.join(os.path.dirname(__file__), '../budgeting_schema.sql')

        with open(schema_path, 'r') as f:
            cursor.execute(f.read())
            print(f"Created {BUDGETING_DB} tables")

        connection.commit()
        print(f"Initialized database tables")
    except Exception as error:
        print(f"An error occurred with initializing database tables: {error}")
    finally:
        if cursor is not None: cursor.close()
        if connection is not None: connection.close()
