import mysql.connector
import duckdb
import pandas as pd
from mysql.connector import Error

try:
    # Connect to MySQL
    mysql_conn = mysql.connector.connect(
        host="mysql-rfam-public.ebi.ac.uk",
        port=4497,
        database="Rfam",
        user="rfamro"
    )
    
    # Connect to DuckDB
    duck_conn = duckdb.connect('direct_copy.duckdb')
    
    if mysql_conn.is_connected():
        print("Successfully connected to Rfam database")
        
        cursor = mysql_conn.cursor()
        tables = ["family", "clan", "features", "author", "genome"]
        
        for table in tables:
            try:
                print(f"\nProcessing table: {table}")
                
                # Get the data
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                
                if rows:
                    # Get column names
                    columns = [desc[0] for desc in cursor.description]
                    
                    # Convert to DataFrame
                    df = pd.DataFrame(rows, columns=columns)
                    print(f"Retrieved {len(df)} rows from {table}")
                    
                    # Save to DuckDB
                    duck_conn.execute(f"CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM df")
                    print(f"Saved {table} to DuckDB")
                    
                    # Verify the data
                    count = duck_conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                    print(f"Verified {count} rows in DuckDB table {table}")
                else:
                    print(f"No data found in table {table}")
                    
            except Exception as e:
                print(f"Error processing table {table}: {e}")
        
        # List all tables in DuckDB
        print("\nTables in DuckDB:")
        tables = duck_conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchall()
        for table in tables:
            count = duck_conn.execute(f"SELECT COUNT(*) FROM {table[0]}").fetchone()[0]
            print(f"Table {table[0]}: {count} rows")
            
except Error as e:
    print(f"Error: {e}")
    
finally:
    if 'mysql_conn' in locals() and mysql_conn.is_connected():
        cursor.close()
        mysql_conn.close()
        print("MySQL connection closed")
    if 'duck_conn' in locals():
        duck_conn.close()
        print("DuckDB connection closed") 