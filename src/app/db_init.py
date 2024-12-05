'''
CS3250 - Software Development Methods and Tools - Final Project
Module Name: db_init.py
Description: Database and Database Tables Initialization
Authors: Yedani Mendoza Gurrola, Artem Marsh, Jose Gomez Betancourt, Alexander Gonzalez Ramirez, Rhodes Ferris
'''

import os
import psycopg2
from psycopg2 import sql
import time

# Updated database configuration to match Docker environment
DATABASE_USER = 'postgres'
DATABASE_USER_PWD = 'postgres'
DATABASE_HOST = 'db'  # This should match the service name in docker-compose
DATABASE_PORT = '5432'

POSTGRESQL_DB = 'postgres'
BUDGETING_DB = 'budgeting_db'  # Updated to match docker-compose configuration

def wait_for_db(max_retries=5, delay_seconds=2):
    """Wait for database to become available"""
    for attempt in range(max_retries):
        try:
            connection = psycopg2.connect(
                user=DATABASE_USER,
                password=DATABASE_USER_PWD,
                host=DATABASE_HOST,
                port=DATABASE_PORT,
                database=POSTGRESQL_DB
            )
            connection.close()
            return True
        except psycopg2.OperationalError:
            if attempt < max_retries - 1:
                print(f"Database not ready, waiting {delay_seconds} seconds...")
                time.sleep(delay_seconds)
            continue
    return False

def initialize_database():
    """Initialize the database"""
    connection = None
    cursor = None
    
    if not wait_for_db():
        print("Could not connect to database after multiple attempts")
        return

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
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (BUDGETING_DB,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                sql.SQL(
                    'CREATE DATABASE {};'
                ).format(sql.Identifier(BUDGETING_DB))
            )
            print(f'Created new database: {BUDGETING_DB}')
        connection.commit()
        print(f'Initialized database')
    except Exception as error:
        print(f'An error occurred with initializing the database: {error}')
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def populate_database():
    """Populate the database with initial schema"""
    connection = None
    cursor = None
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

        schema_path = os.path.join(
            os.path.dirname(__file__), 
            '../database/schema.sql'
        )

        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                cursor.execute(f.read())
                print(f'Created {BUDGETING_DB} tables')
            connection.commit()
        else:
            print(f"Schema file not found at {schema_path}")
    except Exception as error:
        print(f'An error occurred with initializing database tables: {error}')
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()