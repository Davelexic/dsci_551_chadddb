import pymysql
import nltk
from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# NLTK setup
nltk.download('punkt')
nltk.download('stopwords')

# Database connection setup for MySQL
connection = pymysql.connect(
    host='52.90.229.197',
    user='userdb',
    password='chaddb',
    db='coffee_sales',  # Default DB, can be changed dynamically
)

# MongoDB connection setup
mongo_client = MongoClient('your-mongo-connection-string')

# Function to process user queries using NLTK
def process_query(query):
    tokens = word_tokenize(query.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

# Function to build SQL queries based on user input
def build_sql_query(tokens):
    if 'transactions' in tokens:
        if 'january' in tokens and '2023' in tokens:
            return "SELECT * FROM transactions WHERE transaction_date BETWEEN '2023-01-01' AND '2023-01-31';"
        else:
            return "SELECT * FROM transactions;"
    elif 'products' in tokens:
        return "SELECT * FROM products;"
    elif 'stores' in tokens:
        return "SELECT * FROM stores;"
    return None

# MySQL functions
def list_mysql_databases():
    with connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES;")
        databases = cursor.fetchall()
    return [db[0] for db in databases]

def search_mysql_database(database_name, query):
    connection.select_db(database_name)
    sql_query = build_sql_query(query)
    if sql_query:
        return execute_sql_query(sql_query)
    return []

def execute_sql_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return results

# MongoDB functions
def list_mongo_databases():
    return mongo_client.list_database_names()

def search_mongo_database(database_name, collection_name, query):
    db = mongo_client[database_name]
    collection = db[collection_name]
    return collection.find(query)

# Format results
def format_results(results):
    if len(results) == 0:
        return "No records found."
    
    output = ""
    for result in results:
        output += str(result) + "\n"
    return output

# Main function
def main():
    print("Welcome to chaddb12! You can query MySQL and MongoDB databases.")
    
    while True:
        user_input = input("Ask a question or type 'exit' to quit: ")
        tokens = process_query(user_input)
        
        if 'exit' in tokens:
            print("Goodbye!")
            break
        
        if 'mysql' in tokens:
            mysql_databases = list_mysql_databases()
            print(f"Available MySQL databases: {mysql_databases}")
            
            for db_name in mysql_databases:
                print(f"Searching in MySQL database: {db_name}")
                results = search_mysql_database(db_name, tokens)
                formatted_output = format_results(results)
                print(formatted_output)

        elif 'mongo' in tokens:
            mongo_databases = list_mongo_databases()
            print(f"Available MongoDB databases: {mongo_databases}")
            
            for db_name in mongo_databases:
                print(f"Searching in MongoDB database: {db_name}")
                results = search_mongo_database(db_name, 'your_collection_name', {})
                formatted_output = format_results(results)
                print(formatted_output)

        else:
            print("Please specify whether you want to query 'mysql' or 'mongo'.")
    
if __name__ == "__main__":
    main()
