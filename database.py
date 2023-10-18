import sqlite3


class Database:
    def __init__(self, database, table):
        super().__init__()
        self.db_name = database
        self.table = table

    def create_database(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute(
            """
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            customer_surname TEXT,
            customer_address TEXT,
            customer_postal INTEGER,
            customer_city TEXT 
        )
        """
        )

        conn.commit()
        conn.close()
        return True

    def insert_data(
        self,
        customer_name: str,
        customer_surname: str,
        customer_address: str,
        customer_postal: int,
        customer_city: str,
    ):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        sample_data = [
            (
                customer_name,
                customer_surname,
                customer_address,
                int(customer_postal),
                customer_city,
            ),
        ]

        c.executemany(
            f"""
        INSERT INTO {self.table} (customer_name,
        customer_surname,
        customer_address,
        customer_postal,
        customer_city)
        VALUES (?, ?, ?, ?, ?)
        """,
            sample_data,
        )

        conn.commit()
        conn.close()
        return True
    def display_data(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute(f"SELECT * FROM {self.table}")

        # Print column names
        column_names = [column[0] for column in c.description]
        print(column_names)

        rows = c.fetchall()

        for row in rows:
            print(row)

        conn.close()

    def delete_table(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute(f"DROP TABLE IF EXISTS {self.table}")

        conn.commit()
        conn.close()

    def delete_row_by_id(self, user_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute(f"DELETE FROM {self.table} WHERE customer_id", (user_id,))

        conn.commit()
        conn.close()
