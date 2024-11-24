import requests
import json
import os
import base64
from datetime import datetime

class DatabaseManager:
    def __init__(self, api_key=None):
        self.owner = "Davelexic"
        self.database = "coffee_sales.db"
        self.api_key = api_key
        self.last_sql_query = None
        
        if not self.api_key:
            raise ValueError("DBHub.io API key is required")

    def process_query(self, query):
        """Process natural language query without NLTK"""
        # Simple tokenization by splitting on spaces and converting to lowercase
        tokens = query.lower().split()
        
        # Basic stopwords list
        stop_words = {'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for',
                     'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on',
                     'that', 'the', 'to', 'was', 'were', 'will', 'with'}
        
        # Filter out stopwords
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

        # Handle top/best selling products first
        if ('top' in tokens or 'best' in tokens) and ('selling' in tokens or 'products' in tokens):
            query = """
                SELECT 
                    p.product_id,
                    p.product_name,
                    p.category,
                    p.price,
                    COALESCE(SUM(td.quantity), 0) as units_sold
                FROM products p
                LEFT JOIN transaction_details td ON p.product_id = td.product_id
                GROUP BY p.product_id, p.product_name, p.category, p.price
                HAVING units_sold > 0
                ORDER BY units_sold DESC
                LIMIT 10;
            """
            self.last_sql_query = query
            return query

        # Normal query processing
        selected_query = None
        for key, query_type in query_mapping.items():
            if any(keyword in tokens for keyword in query_type['keywords']):
                selected_query = query_mapping[key]
                break

        if not selected_query:
            query = "SELECT 'Please ask about sales, products, locations, or summary information.' as message;"
            self.last_sql_query = query
            return query

        # Add price/amount conditions
        try:
            price_index = -1
            for i, token in enumerate(tokens):
                if token in ['under', 'below', 'less']:
                    price_index = i + 1
                    break
                elif token in ['over', 'above', 'more']:
                    price_index = i + 1
                    break

            if price_index >= 0 and price_index < len(tokens):
                amount = float(tokens[price_index].replace('$', ''))
                if 'under' in tokens or 'below' in tokens or 'less' in tokens:
                    selected_query['conditions'].append(
                        f"(td.quantity * td.unit_price) < {amount}"
                    )
                elif 'over' in tokens or 'above' in tokens or 'more' in tokens:
                    selected_query['conditions'].append(
                        f"(td.quantity * td.unit_price) > {amount}"
                    )
        except (ValueError, IndexError):
            pass

        # Add time-based conditions
        if 'recent' in tokens:
            selected_query['conditions'].append(
                "t.transaction_date >= DATE('now', '-7 days')"
            )
        elif 'today' in tokens:
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

        # Combine base query with conditions
        query = selected_query['base']
        if 'conditions' in selected_query and selected_query['conditions']:
            has_where = 'WHERE' in query
            query += f"\n{'AND' if has_where else 'WHERE'} " + " AND ".join(selected_query['conditions'])

        # Add ordering for top transactions
        if ('top' in tokens or 'best' in tokens or 'highest' in tokens) and ('transactions' in tokens or 'sales' in tokens or 'orders' in tokens):
            query += "\nORDER BY total_amount DESC"
        else:
            query += "\nORDER BY t.transaction_date DESC"  # Default ordering by date

        # Add limit if not a summary query
        if 'summary' not in tokens:
            query += "\nLIMIT 10"

        # Store and return the final query
        self.last_sql_query = query + ";"
        return self.last_sql_query

    def execute_query(self, sql_query):
        """Execute query on DBHub.io"""
        print(f"Executing query: {sql_query}")  # Debug print
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
                error_message = f"DBHub.io API error: {response.status_code} - {response.text}"
                print(error_message)  # Debug print
                return error_message
                
        except requests.exceptions.RequestException as e:
            error_message = f"Connection error: {str(e)}"
            print(error_message)  # Debug print
            return error_message

    def search_database(self, natural_query):
        """Search database using natural language query"""
        try:
            print(f"Processing natural query: {natural_query}")  # Debug print
            tokens = self.process_query(natural_query)
            print(f"Tokens: {tokens}")  # Debug print
            sql_query = self.build_query(tokens)
            print(f"Generated SQL: {sql_query}")  # Debug print
            
            if not sql_query:
                return "I don't understand that query. Try asking about sales, products, locations, or summary information."
                
            result = self.execute_query(sql_query)
            print(f"Query result: {result}")  # Debug print
            return result
        except Exception as e:
            error_message = f"Error processing query: {str(e)}"
            print(error_message)  # Debug print
            return error_message