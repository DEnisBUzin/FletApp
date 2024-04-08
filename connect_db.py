import psycopg2 as pc2
import config

class WorkDB:

    def __init__(self, user, password, name_db):
        self.cursor = None
        self.connection = None
        self.user = user
        self.password = password
        self.name_db = name_db

    def connect_db(self):
        self.connection = pc2.connect(user=self.user, password=self.password, database=self.name_db)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        print("[INFO] Connection is closed")


class UseDB(WorkDB):
    def create_structure(self):
        try:
            self.connect_db()
            sql_query_client = """
                        CREATE TABLE IF NOT EXISTS user_inf(
                        id SERIAL PRIMARY KEY, 
                        login VARCHAR(20) NOT NULL, 
                        password VARCHAR(20) NOT NULL, 
                        email VARCHAR(20) NOT NULL,
                        UNIQUE(login, email));
                    """
            self.cursor.execute(sql_query_client)
            self.connection.commit()
            print("[INFO] Tables created successfully.")
        except Exception as err:
            print(f"[ERROR] Failed to create tables: {err}")
        finally:
            self.close_connection()

    def add_new_user(self, login, password, email):
        try:
            self.connect_db()

            sql_query = """
                INSERT INTO user_inf(login, password, email)
                VALUES (%s, %s, %s);
            """
            self.cursor.execute(sql_query, (login, password, email))
            self.connection.commit()
            print("[INFO] Successfully.")
        except Exception as err:
            print(f"[ERROR] Failed to create tables: {err}")
        finally:
            self.close_connection()

    def auth_user(self, login, password):
        try:
            self.connect_db()
            sql_query = """
                SELECT * FROM user_inf
                WHERE login = %s
                AND password = %s;
            """

            self.cursor.execute(sql_query, (login, password))
            answer = self.cursor.fetchall()
            if len(answer) != 0:
                return answer
            else:
                return None
        except Exception as err:
            print(f"Error: {err}")
        finally:
            self.close_connection()


if __name__ == '__main__':

    newClass = UseDB(user=config.USER, password=config.PASSWORD, name_db=config.NAME_DB)
    newClass.create_structure()
    newClass.add_new_user(login='123', password='123', email='123')
    print(newClass.auth_user(login='1234', password='123'))