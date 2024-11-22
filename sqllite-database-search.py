import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import requests
import json
import os
import base64
from datetime import datetime

# NLTK setup
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class DatabaseManager:
    def __init__(self, api_key=None):
        self.owner = "Davelexic"
        self.database = "coffee_sales.db"
        self.api_key = api_key
        
        if not self.api_key:
            raise ValueError("DBHub.io API key is required")

    def process_query(self, query):
        """Process natural language query"""
        tokens = word_tokenize(query.lower())
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]
        return filtered_tokens

    def build_query(self, tokens):
        """Build SQL query based on natural language tokens"""
        # Query mapping for different types of questions
        query_mapping = {
            'sales': {
                'keywords': ['sales', 'transactions', 'orders', 'sold'],
                'base': """
                    SELECT 
                        t.transaction_id,
                        t.transaction_date,
                        p.product_name,
                        td.quantity,
                        td.unit_price,
                        (td.quantity * td.unit_price) as total_amount,
                        l.location_name
                    FROM transactions t
                    JOIN transaction_details td ON t.transaction_id = td.transaction_id
                    JOIN products p ON td.product_id = p.product_id
                    JOIN locations l ON t.location_id = l.location_id
                """,
                'conditions': []
            },
            'products': {
                'keywords': ['products', 'items', 'coffee', 'drinks', 'menu'],
                'base': "SELECT * FROM products",
                'conditions': []
            },
            'locations': {
                'keywords': ['locations', 'stores', 'shops', 'where'],
                'base': "SELECT * FROM locations",
                'conditions': []
            },
            'summary': {
                'keywords': ['summary', 'total', 'overview', 'performance'],
                'base': """
                    SELECT 
                        l.location_name,
                        COUNT(DISTINCT t.transaction_id) as total_transactions,
                        SUM(td.quantity) as total_items_sold,
                        SUM(td.quantity * td.unit_price) as total_revenue
                    FROM transactions t
                    JOIN transaction_details td ON t.transaction_id = td.transaction_id
                    JOIN locations l ON t.location_id = l.location_id
                    GROUP BY l.location_id, l.location_name
                """
            }
        }

        # Determine which query to use based on tokens
        selected_query = None
        for key, query_type in query_mapping.items():
            if any(keyword in tokens for keyword in query_type['keywords']):
                selected_query = query_mapping[key]
                break

        if not selected_query:
            return None

        # Add time-based conditions
        if 'today' in tokens:
            selected_query['conditions'].append(
                "DATE(t.transaction_date) = DATE('now')"
            )
        elif 'yesterday' in tokens:
            selected_query['conditions'].append(
                "DATE(t.transaction_date) = DATE('now', '-1 day')"
            )
        elif 'week' in tokens:
            selected_query['conditions'].append(
                "t.transaction_date >= DATE('now', '-7 days')"
            )
        elif 'month' in tokens:
            selected_query['conditions'].append(
                "t.transaction_date >= DATE('now', '-30 days')"
            )

        # Add ordering if requested
        if any(word in tokens for word in ['best', 'top', 'highest']):
            if 'sales' in tokens:
                selected_query['base'] += "\nGROUP BY p.product_id, p.product_name"
                selected_query['base'] += "\nORDER BY SUM(td.quantity) DESC"

        # Combine base query with conditions
        query = selected_query['base']
        if 'conditions' in selected_query and selected_query['conditions']:
            query += "\nWHERE " + " AND ".join(selected_query['conditions'])

        # Add limit if not a summary query
        if 'summary' not in tokens:
            query += "\nLIMIT 10"

        return query + ";"

    def execute_query(self, sql_query):
        """Execute query on DBHub.io"""
        encoded_sql = base64.b64encode(sql_query.encode('utf-8')).decode('utf-8')
        
        form_data = {
            'apikey': self.api_key,
            'dbowner': self.owner,
            'dbname': self.database,
            'sql': encoded_sql
        }
        
        try:
            response = requests.post(
                'https://api.dbhub.io/v1/query',
                data=form_data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.RequestException as e:
            return f"Connection error: {str(e)}"

    def search_database(self, natural_query):
        """Search database using natural language query"""
        tokens = self.process_query(natural_query)
        sql_query = self.build_query(tokens)
        
        if not sql_query:
            return "I don't understand that query. Try asking about sales, products, locations, or summary information."
            
        return self.execute_query(sql_query)

    def format_results(self, results):
        """Format results for display"""
        if not results:
            return "No results found."
            
        if isinstance(results, str):  # Error message
            return results
            
        output = "\nResults:\n"
        output += "=" * 50 + "\n"
        
        if isinstance(results, list):
            for row in results:
                if isinstance(row, list):
                    row_data = []
                    for col in row:
                        if isinstance(col, dict) and 'Value' in col:
                            row_data.append(str(col['Value']))
                    output += " | ".join(row_data) + "\n"
                else:
                    output += str(row) + "\n"
                    
        return output

def main():
    print("Coffee Sales Natural Language Query System")
    print("\nExample questions you can ask:")
    print("- Show me today's sales")
    print("- What are our best selling products?")
    print("- Show me all store locations")
    print("- Give me a sales summary")
    print("- What products do we sell?")
    print("- Show me last week's transactions")
    print("- What are the top selling items this month?")
    
    # Get API key from environment variable or user input
    api_key = os.environ.get('DBHUB_API_KEY')
    if not api_key:
        api_key = input("Please enter your DBHub.io API key: ")
    
    db_manager = DatabaseManager(api_key)
    
    while True:
        query = input("\nWhat would you like to know? (type 'exit' to quit): ")
        
        if query.lower() == 'exit':
            print("Goodbye!")
            break
            
        results = db_manager.search_database(query)
        print(db_manager.format_results(results))

if __name__ == "__main__":
    main()