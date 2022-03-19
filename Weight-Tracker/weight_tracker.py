import mariadb
import sys
from datetime import date
from decimal import Decimal

try:
    conn = mariadb.connect(
        user="<username>",
        password="<password>",
        host="0.0.0.0",
        port=3306,
        database="weight"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()

# If database empty populate with placeholder values
try:
    cur.execute("SELECT ID FROM weight ORDER BY ID DESC LIMIT 1;")
    prev_id = Decimal(cur.fetchall()[0][0])
except:
    cur.execute("INSERT INTO weight VALUES (0,0,0,0,0,0,0);")

# Find previous entry ID, inc by 1.
try:
    cur.execute("SELECT ID FROM weight ORDER BY ID DESC LIMIT 1;")
    prev_id = Decimal(cur.fetchall()[0][0])
    id = prev_id + 1
except:
    id = 0

# Set goal weight
goal = 100

# Get todays date
the_date = date.today()

# Get weight from cli
new_weight = Decimal((sys.argv[1]))

# Calculate average of last 30 days
total = 0
cur.execute("SELECT weight FROM weight ORDER BY ID DESC LIMIT 7")
weeks_weight = cur.fetchall()
if len(weeks_weight) == 7:
    for list in weeks_weight:
        total = total + Decimal(list[0])
    new_average = round(total / 7, 2)
else:
    new_average = 0

# Calculate difference in weight from last entry
cur.execute("SELECT weight FROM weight WHERE id=%s",(prev_id,))
old_weight = Decimal(cur.fetchall()[0][0])
new_difference = new_weight - old_weight
if new_difference > 100:
    new_difference = 0

# Total Diff
total_diff = 0
cur.execute("SELECT difference FROM weight;")
all_diffs = cur.fetchall()
for result in all_diffs:
    for num in result:
        total_diff += Decimal(num)
total_diff += new_difference
if total_diff > 100:
    total_diff = 0

# Commit new entry to database
sql_insert = "INSERT INTO weight (ID, weight, average, difference, date, goal, total_difference) VALUES (%s, %s, %s, %s, %s, %s, %s);"
cur.execute(sql_insert,(id, new_weight, new_average, new_difference, the_date, goal, total_diff))
conn.commit()

sql_get = f"SELECT weight, average, difference, date, total_difference FROM weight WHERE ID={id};"
cur.execute(sql_get)
results = cur.fetchall()
print(f"Weight = {results[0][0]}")
print(f"Average = {results[0][1]}")
print(f"Difference = {results[0][2]}")
print(f"Date = {results[0][3]}")
print(f"Total Difference = {results[0][4]}")
