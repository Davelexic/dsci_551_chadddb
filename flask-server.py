from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from datetime import datetime
from typing import Dict, List, Union, Optional

# Import your existing DatabaseManager
from sqllite_database_search import DatabaseManager

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class MongoDBManager:
    def __init__(self, connection_string: str, database_name: str):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
    
    def process_query(self, collection_name: str, query_params: Dict) -> List[Dict]:
        """Execute MongoDB query based on parameters"""
        collection = self.db[collection_name]
        
        # Build MongoDB query from parameters
        mongo_query = {}
        if 'date_from' in query_params:
            mongo_query['timestamp'] = {
                '$gte': datetime.fromisoformat(query_params['date_from'])
            }
        if 'date_to' in query_params:
            if 'timestamp' in mongo_query:
                mongo_query['timestamp']['$lte'] = datetime.fromisoformat(query_params['date_to'])
            else:
                mongo_query['timestamp'] = {
                    '$lte': datetime.fromisoformat(query_params['date_to'])
                }
        
        # Add any other query parameters
        for key, value in query_params.items():
            if key not in ['date_from', 'date_to']:
                mongo_query[key] = value
        
        return list(collection.find(mongo_query))

class QueryRouter:
    def __init__(self):
        # Initialize SQL database manager
        self.sql_manager = DatabaseManager(api_key=os.getenv('DBHUB_API_KEY'))
        
        # Initialize MongoDB manager
        mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
        mongo_db = os.getenv('MONGODB_DB', 'coffee_analytics')
        self.mongo_manager = MongoDBManager(mongo_uri, mongo_db)
    
    def determine_database(self, query: str) -> str:
        """Determine which database to query based on the natural language input"""
        # Keywords that indicate MongoDB usage
        mongo_keywords = ['analytics', 'metrics', 'dashboard', 'trend', 'analysis']
        
        # Check if query contains MongoDB-specific keywords
        if any(keyword in query.lower() for keyword in mongo_keywords):
            return 'mongodb'
        return 'sql'  # Default to SQL for traditional queries
    
    def process_query(self, query: str) -> Dict:
        """Process the query and route to appropriate database"""
        database_type = self.determine_database(query)
        
        try:
            if database_type == 'mongodb':
                # Extract relevant parameters for MongoDB query
                # This is a simplified example - you might want to use NLP to extract more parameters
                collection_name = 'sales_analytics'
                query_params = {
                    'date_from': datetime.now().isoformat()[:10]  # Today's date
                }
                results = self.mongo_manager.process_query(collection_name, query_params)
            else:
                results = self.sql_manager.search_database(query)
            
            return {
                'status': 'success',
                'data': results,
                'database_used': database_type
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
    
    result = query_router.process_query(data['query'])
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
    
    # Extract headers from first result
    headers = list(results[0].keys())
    
    # Convert results to table format
    table = [headers]
    for result in results:
        row = [str(result.get(header, '')) for header in headers]
        table.append(row)
    
    return table

@app.route('/api/query/table', methods=['POST'])
def query_table():
    """API endpoint that returns results in table format"""
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({
            'status': 'error',
            'message': 'No query provided'
        }), 400
    
    result = query_router.process_query(data['query'])
    
    if result['status'] == 'success':
        table_data = format_results_as_table(result['data'])
        return jsonify({
            'status': 'success',
            'data': table_data,
            'database_used': result['database_used']
        })
    
    return jsonify(result)

if __name__ == '__main__':
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run the Flask app
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
