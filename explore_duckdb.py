import duckdb
import os

def explore_database(db_file):
    print(f"\nExploring {db_file}:")
    conn = duckdb.connect(db_file)
    
    # List all tables
    print("\nAvailable tables:")
    tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchall()
    
    if not tables:
        print("No tables found in the database.")
        conn.close()
        return
        
    for table in tables:
        print(f"\n=== Table: {table[0]} ===")
        # Get column information
        columns = conn.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table[0]}'").fetchall()
        print("\nColumns:")
        for col in columns:
            print(f"{col[0]}: {col[1]}")
        # Show first few rows
        print("\nFirst 5 rows:")
        try:
            rows = conn.execute(f"SELECT * FROM {table[0]} LIMIT 5").fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Error reading table: {e}")
        print("\n" + "="*50)

    conn.close()

# List all .duckdb files in the current directory
duckdb_files = [f for f in os.listdir('.') if f.endswith('.duckdb')]
print("Available DuckDB files:")
for i, file in enumerate(duckdb_files, 1):
    print(f"{i}. {file}")

# Explore both databases
for db_file in duckdb_files:
    explore_database(db_file) 