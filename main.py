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
        UPDATE all_reviews
        SET content = 'awesome place'
        WHERE id = 1;





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
             
    @app.route('/newreview', methods=['POST'])
    def newreview():
        try:
            connection = psycopg2.connect(**db_config)
            cursor = connection.cursor()

            # Extract user data from the request
            data = request.get_json()
            rating = data.get('rating')
            content = data.get('content')
            brewery_name=data.get('brewery_name')
            username=data.get('username')
            # Insert user data into the 'users' table
            insert_sql = "INSERT INTO all_reviews (rating, content, brewery_name,username) VALUES (%s, %s,%s,%s)"
            cursor.execute(insert_sql, (rating, content,brewery_name,username))
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
            data = request.get_json()
            username = data.get('username')
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
        
    @app.route('/allreviews', methods=['GET'])
    def get_all_reviews():
        try:
            connection = psycopg2.connect(**db_config)
            cursor = connection.cursor()
            brewery_name = request.args.get('brewery_name')
            print(brewery_name)
            # Select all rows from the 'reviews' table (assuming you have a 'reviews' table)
            select_sql = "SELECT * FROM all_reviews where brewery_name= %s"
            cursor.execute(select_sql,(brewery_name,))
            rows = cursor.fetchall()

            cursor.close()
            connection.close()

            # Convert the rows to a list of dictionaries
            reviews = []
            for row in rows:
                review = {
                    'id': row[0],
                    'brewery_name': row[1],
                    'username': row[2],
                    'rating':row[3],
                    'content':row[4]
                    
                    # Add other review attributes as needed
                }
                reviews.append(review)

            return jsonify(reviews)
        except Exception as e:
            return str(e)
        
    @app.route('/filterresult', methods=['POST'])
    def filter_breweries():
        data = request.get_json()
        by_city = data.get('by_city','')
        by_type = data.get('by_type','')
        by_name = data.get('by_name','')
        print(by_city)
        print(by_name)
        print(by_type)
        # Construct the query parameters
        params = {
            'by_city': by_city,
            'by_type': by_type,
            'by_name': by_name,
        }

        # Make a request to the Open Brewery Database API
        apiurl = 'https://api.openbrewerydb.org/v1/breweries'
        params = {
        key: value for key, value in {
            'by_city': by_city,
            'by_type': by_type,
            'by_name': by_name,
        }.items() if value
        }
        response = requests.get(apiurl, params=params)
        if response.status_code == 200:
            # Successful response
            result_data = response.json()
            print(result_data)
            return {'data': result_data}
        else:
            # Error occurred while fetching data
            error_message = f"Error: {response.status_code} - {response.text}"
            return jsonify({'data': [], 'error': error_message}), response.status_code
        

    


if __name__ == '__main__':
    app.run(debug=True)
