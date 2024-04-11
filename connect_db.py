import psycopg2 as pc2
import config


class WorkDB:
    '''Класс соединения базы данных'''
    def __init__(self, user, password, name_db):
        self.cursor = None
        self.connection = None
        self.user = user
        self.password = password
        self.name_db = name_db

    def connect_db(self):
        '''Функция соединения базы данных'''
        self.connection = pc2.connect(user=self.user, password=self.password, database=self.name_db)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        '''Функция закрытия соединения базы данных'''
        self.cursor.close()
        self.connection.close()
        print("[INFO] Connection is closed")


class UseDB(WorkDB):
    '''Класс запросов к базе данных'''
    def create_structure(self):
        '''Функция создания структуры'''
        try:
            self.connect_db()
            sql_query_client = """
                        CREATE TABLE IF NOT EXISTS user_inf(
                        id SERIAL PRIMARY KEY, 
                        login VARCHAR(20) NOT NULL, 
                        password VARCHAR(20) NOT NULL, 
                        division VARCHAR(20) NOT NULL,
                        name VARCHAR(20) NOT NULL,
                        surname VARCHAR(20) NOT NULL,
                        zvanie VARCHAR(40) NOT NULL,
                        UNIQUE(login));
                    """
            self.cursor.execute(sql_query_client)
            self.connection.commit()
            print("[INFO] Tables created successfully.")
        except Exception as err:
            print(f"[ERROR] Failed to create tables: {err}")
        finally:
            self.close_connection()

    def add_new_user(self, login, password, division, name, surname, zvanie):
        '''Функция добавления нового пользователя'''
        try:
            self.connect_db()

            sql_query = """
                INSERT INTO user_inf(login, password, division, name, surname, zvanie)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            self.cursor.execute(sql_query, (login, password, division, name, surname, zvanie))
            self.connection.commit()
            print("[INFO] Successfully.")
        except Exception as err:
            print(f"[ERROR] Failed to create tables: {err}")
        finally:
            self.close_connection()

    def auth_user(self, login, password):
        '''Функция авторизации'''
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
    newClass.add_new_user(login='123', password='123', division='123')
    print(newClass.auth_user(login='1234', password='123'))