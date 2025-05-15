import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host="mysql-rfam-public.ebi.ac.uk",
        port=4497,
        database="Rfam",
        user="rfamro"
    )
    
    if connection.is_connected():
        print("Successfully connected to Rfam database")
        
        cursor = connection.cursor()
        
        # Test query on family table
        cursor.execute("SELECT COUNT(*) FROM family")
        result = cursor.fetchone()
        print(f"Number of rows in family table: {result[0]}")
        
        # Get some sample data
        cursor.execute("SELECT * FROM family LIMIT 5")
        rows = cursor.fetchall()
        print("\nSample data from family table:")
        for row in rows:
            print(row)
            
except Error as e:
    print(f"Error connecting to MySQL database: {e}")
    
finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed.") 