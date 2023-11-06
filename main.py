from flask import Flask,request,jsonify
import requests
from flask_cors import CORS
import psycopg2

import json

app = Flask(__name__)
CORS(app)
db_config = {
    'user': 'siddhant',
    'password': 'asphalt9',
    'host': 'database-1.cdfwcjl1s19w.ap-south-1.rds.amazonaws.com',
    'database': 'siddhant_tyagi'
}



class endpoints:
    
    @app.route('/info',methods=['POST'])
    def website_info():
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            username varchar(50),
            password varchar(50)
           
        );
        """
        
        cursor.execute(create_table_sql)
        connection.commit()
        cursor.close()
        connection.close()
        return "Table created successfully."
        
    @app.route('/insert_user', methods=['POST'])
    def insert_user():
        try:
            connection = psycopg2.connect(**db_config)
            cursor = connection.cursor()

            # Extract user data from the request
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            # Insert user data into the 'users' table
            insert_sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(insert_sql, (username, password))
            connection.commit()
            cursor.close()
            connection.close()

            return "User data inserted successfully."
        except Exception as e:
            return str(e)       

    @app.route('/get_all_users', methods=['GET'])
    def get_all_users():
        try:
            connection = psycopg2.connect(**db_config)
            cursor = connection.cursor()

            # Select all rows from the 'users' table
            select_sql = "SELECT * FROM users"
            cursor.execute(select_sql)
            rows = cursor.fetchall()

            cursor.close()
            connection.close()

            # Convert the rows to a list of dictionaries
            users = []
            for row in rows:
                user = {
                    'id': row[0],
                    'username': row[1],
                    'password': row[2]
                }
                users.append(user)

            return jsonify(users)
        except Exception as e:
            return str(e)


if __name__ == '__main__':
    app.run(debug=False)
