from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from typing import Dict, List, Union, Optional
import json
from bson import json_util

# At the top of your flask-server.py
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("dotenv not found, skipping environment variable loading")
    # Simple alternative to load_dotenv
    def load_dotenv():
        pass
# Import your existing SQLite DatabaseManager
from sqlite_database_search import DatabaseManager
from nosql_query_parser import parse_query,build_pipeline,execute_pipeline

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class QueryRouter:
    def __init__(self):
        # Initialize SQL database manager with your DBHub.io API key
        self.sql_manager = DatabaseManager(api_key=os.getenv('DBHUB_API_KEY'))
        # pass
    
    def process_query(self, query: str, database_type: str) -> Dict:
        """Process the query based on selected database type"""
        try:
            if database_type == 'mongodb':
                try:
                    # print("here")
                    collection, field, condition, value = parse_query(query)
                    pipeline = build_pipeline(field, condition, value)
                    # print(pipeline,collection)
                    results,nosql_pipeline = execute_pipeline(collection, pipeline)
                    results = json.dumps(results,default=json_util.default)
                    results = json.loads(results)
                    nosql_pipeline = json.dumps(nosql_pipeline,default=json_util.default)
                    nosql_pipeline = json.loads(nosql_pipeline)
                    # print(results)
                    return {
                        'status': 'success',
                        'data': results,
                        'query': nosql_pipeline,
                        'database_used': database_type
                    }
                except Exception as e:
                    # print(f"Error: {e}")
                    return {
                        'status': 'error',
                        'message': str(e),
                        'database_used': database_type
                    }
                
            else:  # SQLite
                results = self.sql_manager.search_database(query)
                return {
                    'status': 'success',
                    'data': results,
                    'database_used': 'sqlite'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'database_used': database_type
            }

# Initialize the query router
query_router = QueryRouter()

@app.route('/api/query', methods=['POST'])
def process_query():
    """API endpoint to process natural language queries"""
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({
            'status': 'error',
            'message': 'No query provided'
        }), 400
    
    database_type = data.get('database_type', 'sqlite')  # Default to SQLite
    result = query_router.process_query(data['query'], database_type)
    return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

def format_results_as_table(results: List[Dict]) -> List[List]:
    """Convert results to a table format"""
    if not results:
        return []
    
    if isinstance(results, str):
        return [[results]]
    
    if isinstance(results, list) and results and isinstance(results[0], list):
        return results
    
    # Extract headers from first result
    if isinstance(results[0], dict):
        headers = list(results[0].keys())
        
        # Convert results to table format
        table = [headers]
        for result in results:
            row = [str(result.get(header, '')) for header in headers]
            table.append(row)
        return table
    
    return [[str(item)] for item in results]

@app.route('/api/query/table', methods=['POST'])
def query_table():
    """API endpoint that returns results in table format"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No query provided'
            }), 400
        
        database_type = data.get('database_type', 'sqlite')
        result = query_router.process_query(data['query'], database_type)
        # print("in query table: ",result)
        if result['status'] == 'success':
            # Add default column headers based on query type
            if(result['database_used'] == 'mongodb'):
                return jsonify({
                'status': 'success',
                'data': result['data'],
                'sql_query': result['query'],
                'database_used': result['database_used']
            })
            
            if isinstance(result['data'], list) and result['data']:
                if 'locations' in data['query'].lower():
                    headers = ['location_id', 'location_name']
                elif 'products' in data['query'].lower():
                    headers = ['product_id', 'product_name', 'category', 'price']
                elif 'sales' in data['query'].lower():
                    headers = ['transaction_id', 'transaction_date', 'product_name', 'quantity', 'unit_price', 'total_amount', 'location_name']
                else:
                    # Extract headers from the first row if no specific headers match
                    headers = [k for k in result['data'][0].keys()] if isinstance(result['data'][0], dict) else []

                # Format the data with headers
                table_data = [headers] + [
                    [str(cell.get('Value', '')) if isinstance(cell, dict) else str(cell) 
                     for cell in row]
                    for row in result['data']
                ]
                print("print table data",table_data)
            else:
                table_data = []

            return jsonify({
                'status': 'success',
                'data': table_data,
                'sql_query': query_router.sql_manager.last_sql_query,
                'database_used': result['database_used']
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Make sure DBHUB_API_KEY is set
    if not os.getenv('DBHUB_API_KEY'):
        raise ValueError("DBHUB_API_KEY environment variable is required")
    
    # Run the Flask app
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))