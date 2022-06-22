from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

import uuid

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection
        
    def add_user(self, username, password):
        # check user existence
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM user 
        WHERE username = %s;
        """, (username,))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'username': row['username']
            })
        # user existed - return msg 
        if result:
            cursor.close()
            return "User existed. Please Log In."
        
        # user doesn't exist - register new user, return msg 
        else:
            cursor = self.connection.cursor(dictionary=True)
            generateUUID = str(uuid.uuid4())
            cursor.execute("""
            INSERT INTO user (id, username, password)
            VALUES (%s, %s, %s);
            """, (generateUUID, username, password))
            cursor.close()
            self.connection.commit()
            return "New user successfully registered!"
    
    # get user for login
    def get_user(self, username, password):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM user 
        WHERE username = %s AND password = %s;
        """, (username, password))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'username': row['username']
            })
        cursor.close()
        return result
    
    def upload_file (self, content, owner):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM storage
        WHERE content = %s AND owner = %s;
        """,(content, owner))
        for row in cursor.fetchall():
            result.append({
                'content': row['content'],
                'owner': row['owner']
            })
        if result:
            cursor.close()
            return "File existed. Please upload a different file."
        else:
            generateUUID = str(uuid.uuid4())
            cursor.execute("""
            INSERT INTO storage (id, content, owner)
            VALUES (%s, %s, %s);
            """, (generateUUID, content, owner))
            cursor.close()
            self.connection.commit()
            return "File successfully uploaded!"
        
    def download_file(self, uuid, currentUser):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM storage
        WHERE id = %s;
        """, (uuid,))
        for row in cursor.fetchall():
            result.append({
                'owner' : row['owner']
            })
        
        if result:
            if result[0]['owner'] == currentUser:
                result.clear()
                cursor.execute("""
                SELECT * FROM storage
                WHERE id = %s;
                """, (uuid,))
                for row in cursor.fetchall():
                    result.append({
                        'content' : row['content']
                    })
                cursor.close()
                return result
            else:
                cursor.close()
                return "Download prohibited, current user is not the file owner."   
        else:
            cursor.close()
            return "No file matches this ID."
        
    def get_all_file(self, currentUser):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM storage
        WHERE owner = %s;
        """,(currentUser,))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'content': row['content']
            })
            cursor.close()
        if result:
            return result
        else:
            return "No file uploaded by " + currentUser
        
class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='soa',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)
    
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())