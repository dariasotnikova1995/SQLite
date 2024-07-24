import sqlite3
from typing import List, Type, TypeVar, Generic, Any

T = TypeVar('T')

class Record:
    """A base class for database records."""
    def to_tuple(self):
        raise NotImplementedError("Subclasses must implement this method")

class DatabaseTable(Generic[T]):
    def __init__(self, db_name: str, table_name: str, record_type: Type[T], create_table_sql: str):
        self.db_name = db_name
        self.table_name = table_name
        self.record_type = record_type
        self.create_table_sql = create_table_sql

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(self.create_table_sql)
            conn.commit()

    def get_all_records(self) -> List[T]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            rows = cursor.fetchall()
            return [self.record_type(*row) for row in rows]

    def add_records(self, records: List[T]):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            for record in records:
                cursor.execute(f"INSERT INTO {self.table_name} VALUES ({', '.join('?' for _ in range(len(record.to_tuple())))})", record.to_tuple())
            conn.commit()

    def update_record(self, set_clause: str, condition: str):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {self.table_name} SET {set_clause} WHERE {condition}")
            conn.commit()

    def get_records_by_condition(self, condition: str) -> List[T]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE {condition}")
            rows = cursor.fetchall()
            return [self.record_type(*row) for row in rows]

    def delete_records_by_condition(self, condition: str):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {self.table_name} WHERE {condition}")
            conn.commit()

class Person(Record):
    def __init__(self, name: str, favorite_color: str, profit: float):
        self.name = name
        self.favorite_color = favorite_color
        self.profit = profit

    def to_tuple(self):
        return (self.name, self.favorite_color, self.profit)

    def __repr__(self):
        return f"Person(name={self.name}, favorite_color={self.favorite_color}, profit={self.profit})"

create_persons_table_sql = '''
CREATE TABLE IF NOT EXISTS Persons (
    name TEXT,
    favorite_color TEXT,
    profit REAL
)
'''

persons_table = DatabaseTable('example.db', 'Persons', Person, create_persons_table_sql)

persons_table.add_records([
    Person('John', 'red', 1000),
    Person('Anna', 'red', 2000),
    Person('James', 'green', 500),
    Person('Karl', 'black', 2500)
])

# Get all records
all_persons = persons_table.get_all_records()
print("All persons:", all_persons)

# Get records by condition
red_persons = persons_table.get_records_by_condition("favorite_color = 'red'")
print("Red persons:", red_persons)

# Update a record
persons_table.update_record("profit = 3000", "name = 'Anna'")

# Get the updated record
updated_person = persons_table.get_records_by_condition("name = 'Anna'")
print("Updated Anna:", updated_person)

# Delete records by condition
persons_table.delete_records_by_condition("profit < 1000")

# Get all records after deletion
all_persons_after_deletion = persons_table.get_all_records()
print("All persons after deletion:", all_persons_after_deletion)