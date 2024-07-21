import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()

# Create table Persons
c.execute('''
CREATE TABLE IF NOT EXISTS Persons (
    name TEXT,
    favorite_color TEXT,
    profit REAL
)
''')

# Create table Cars
c.execute('''
CREATE TABLE IF NOT EXISTS Cars (
    model TEXT,
    color TEXT,
    price REAL
)
''')

# Insert data into Persons
c.executemany('''
INSERT INTO Persons (name, favorite_color, profit) VALUES (?, ?, ?)
''', [
    ('John', 'red', 1000),
    ('Anna', 'red', 2000),
    ('James', 'green', 500),
    ('Karl', 'black', 2500)
])

# Insert data into Cars
c.executemany('''
INSERT INTO Cars (model, color, price) VALUES (?, ?, ?)
''', [
    ('BMW M1', 'blue', 700),
    ('BMW M2', 'black', 1700),
    ('BMW M3', 'black', 2300),
    ('Fiat M1', 'red', 1500),
    ('Fiat M2', 'red', 1000),
    ('Chevrolet M1', 'green', 501)
])

# Commit the changes
conn.commit()

# Query for task 5: Find the cheapest car each person can afford of their favorite color
c.execute('''
SELECT
    p.name,
    c.model,
    c.color,
    c.price,
    p.profit
FROM
    Persons p
JOIN
    (SELECT model, color, price
     FROM Cars c1
     WHERE price = (SELECT MIN(price)
                    FROM Cars c2
                    WHERE c1.color = c2.color)) c
ON
    p.favorite_color = c.color
WHERE
    c.price <= p.profit
ORDER BY
    p.name ASC
''')
result_task_5 = c.fetchall()
print("Result for task 5:")
for row in result_task_5:
    print(row)

# Query for task 6: Find the cheapest car each person can afford, or NULL if they can't afford any
c.execute('''
SELECT
    p.name,
    COALESCE(c.model, '') AS model,
    COALESCE(c.color, p.favorite_color) AS color,
    COALESCE(c.price, '') AS price,
    p.profit
FROM
    Persons p
LEFT JOIN
    (SELECT model, color, price
     FROM Cars c1
     WHERE price = (SELECT MIN(price)
                    FROM Cars c2
                    WHERE c1.color = c2.color)) c
ON
    p.favorite_color = c.color AND c.price <= p.profit
ORDER BY
    p.name ASC
''')
result_task_6 = c.fetchall()
print("Result for task 6:")
for row in result_task_6:
    print(row)

# Close the connection
conn.close()