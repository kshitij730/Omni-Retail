import sqlite3
import os
import json

def get_db_connection(db_name: str):
    """Returns a connection to the specified database."""
    # Assuming run from root omni_retail or similar, adjust path
    # We look for data/ folder relative to current working dir or this file
    
    # Try absolute path first if we can guess it, or relative
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    db_path = os.path.join(data_dir, db_name)
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database {db_name} not found at {db_path}")
        
    return sqlite3.connect(db_path)

def execute_sql_query(db_name: str, query: str) -> str:
    """Executes a SQL query against the given DB and returns JSON string results."""
    try:
        conn = get_db_connection(db_name)
        cursor = conn.cursor()
        cursor.execute(query)
        
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
            
        conn.close()
        return json.dumps(results)
    except Exception as e:
        return json.dumps({"error": str(e)})

def get_schema(db_name: str) -> str:
    """Returns the schema of the database as a string."""
    conn = get_db_connection(db_name)
    cursor = conn.cursor()
    
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_str = f"Schema for {db_name}:\n"
    for table in tables:
        schema_str += table[0] + "\n"
        
    conn.close()
    return schema_str
