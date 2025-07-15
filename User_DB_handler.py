import pymysql
import datetime as dt

class SecurityMonitor:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect_db()
        self.create_table()
    def create_table(self):
        try:
            users_query = """
            CREATE TABLE IF NOT EXISTS users(
                user_id varchar(50) unique not null primary key,
                username varchar(50) not null,
                password varchar(120) not null)
            """
            self.cursor.execute(users_query)
            self.connection.commit()
            logs_query="""
            CREATE TABLE IF NOT EXISTS login_logs(
                user_id varchar(50),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                actions varchar(50) not null,
                foreign key(user_id) references users(user_id)
            )"""
            self.cursor.execute(logs_query)
            self.connection.commit()
            print("Tables created")
        except pymysql.Error as e:
            print(f"Error creating table: {e}")
    def connect_db(self):
        self.connection= pymysql.connect(
            host='localhost',
            user='root',
            password="Hwtacbf4!",
            database='user_db')
        self.cursor=self.connection.cursor()
    def validate(self, user_id):
        try:
            self.cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE user_id = %s)", (user_id,))
            result = self.cursor.fetchone()
            if result:
                return bool(result[0])
            return False
        except pymysql.Error as e:
            print(f"Error connecting to database: {e}")
            return False
    def validate_login(self,user_id,password):
        try:
            self.cursor.execute("select password from users where user_id=%s",(user_id,))
            result=self.cursor.fetchone()
            if result and self.check_bruting(user_id) is False:
                stored_hash = result[0]
                return stored_hash == password
            else:
                self.cursor.execute("insert into login_logs(user_id,actions) values(%s,'failed')", (user_id,))
                self.connection.commit()
                return False
        except pymysql.Error as e:
            print(f"Error validating login{e}")
            return False
    def add_user(self,user_id, username , password):
        try:
            query="insert into users(user_id,username,password)values(%s,%s,%s)"
            self.cursor.execute(query,(user_id,username,password))
            self.connection.commit()
            print("Signup successfull")
            return True
        except pymysql.Error as e:
            print(f"Error signing up{e}")
            return False
    def check_bruting(self,user_id):
        query = """select count(*) from login_logs where actions='failed' and timestamp > (now() - interval 2 minute)"""
        self.cursor.execute(query,(user_id,))
        attempts = self.cursor.fetchone()[0]
        if attempts >= 5:
            print("Too many failed attempts. Try again later.")
            return True
        else:
            self.cursor.execute("insert into login_logs(user_id,actions) values(%s,'failed')", (user_id,))
            self.connection.commit()
            return False
    def close_connection(self):
        self.cursor.close()
        self.connection.close()
