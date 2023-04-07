import sqlite3

# Connect to the database
conn = sqlite3.connect('db.sqlite3')

# Define the query to retrieve the mse and ssim_score data
query = 'SELECT x, y FROM charts_imagemetrics;'

try:
    # Execute the query and fetch the data
    data = conn.execute(query).fetchall()

    # Close the database connection
    conn.close()

    mse_data = [row[0] for row in data]
    ssim_data = [row[1] for row in data]

except Exception as e:
    print(f"Error: {e}")