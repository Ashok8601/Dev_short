import sqlite3

# Connect to the database
conn = sqlite3.connect('matsya.db')
cursor = conn.cursor()

# Execute the query
cursor.execute("SELECT username, profile_photo FROM user")

# Fetch and print all results
results = cursor.fetchall()
for row in results:
    print(f"Username: {row[0]}, Profile Photo: {row[1]}")

# Close the connection
conn.close()