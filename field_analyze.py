import pymongo
from typing import Dict, Any, Tuple
import numpy as np

class MongoFieldClassifier:
    def __init__(self, connection_string: str, database_name: str):
        """
        Initialize the MongoDB connection and field classifier
        
        Args:
            connection_string (str): MongoDB connection string
            database_name (str): Name of the database to analyze
        """
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[database_name]
        self.field_types = {}
        self.dimensions = []
        self.metrics = []

    def analyze_collection(self, collection_name: str, sample_size: int = 1000):
        """
        Analyze fields in a given collection
        
        Args:
            collection_name (str): Name of the collection to analyze
            sample_size (int): Number of documents to sample
        """
        collection = self.db[collection_name]
        sample_docs = list(collection.aggregate([{'$sample': {'size': sample_size}}]))
        
        # Reset previous analysis
        self.field_types = {}
        self.dimensions = []
        self.metrics = []
        
        # Analyze each document
        for doc in sample_docs:
            self._process_document(doc)
        
        # Classify fields
        self._classify_fields()
        
        return self.field_types

    def _process_document(self, doc: Dict[str, Any], prefix: str = ''):
        """
        Recursively process document fields
        
        Args:
            doc (dict): Document to process
            prefix (str): Prefix for nested fields
        """
        for key, value in doc.items():
            full_key = f"{prefix}{key}" if prefix else key
            
            # Handle nested documents
            if isinstance(value, dict):
                self._process_document(value, f"{full_key}.")
            else:
                # Determine and track field types
                field_type = self._determine_field_type(value)
                
                if full_key not in self.field_types:
                    self.field_types[full_key] = {
                        'type': field_type,
                        'samples': [value]
                    }
                else:
                    # Limit samples to 5 to prevent excessive memory use
                    if len(self.field_types[full_key]['samples']) < 5:
                        self.field_types[full_key]['samples'].append(value)

    def _determine_field_type(self, value: Any) -> str:
        """
        Determine the type of a field value
        
        Args:
            value: Value to determine type for
        
        Returns:
            str: Classified field type
        """
        if value is None:
            return 'null'
        elif isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, int):
            return 'integer'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, str):
            return 'string'
        elif isinstance(value, list):
            return 'array'
        elif isinstance(value, dict):
            return 'object'
        else:
            return 'unknown'

    def _classify_fields(self):
        """
        Classify fields into dimensions and metrics
        """
        for field, details in self.field_types.items():
            # Heuristics for classification
            if details['type'] in ['integer', 'float']:
                # Potential metric if values have variation
                samples = details['samples']
                if len(set(samples)) > 1:
                    self.metrics.append(field)
            elif details['type'] in ['string', 'object']:
                # Potential dimension for categorical or nested fields
                self.dimensions.append(field)

    def get_classification_summary(self):
        """
        Get summary of field classifications
        
        Returns:
            dict: Summary of dimensions and metrics
        """
        return {
            'total_fields': len(self.field_types),
            'dimensions': self.dimensions,
            'metrics': self.metrics,
            'field_types': self.field_types
        }

# Example usage
def main():
    # Replace with your actual MongoDB connection string
    CONNECTION_STRING = "mongodb://localhost:27017/"
    DATABASE_NAME = "chatdb"
    COLLECTION_NAME = "video-game-sales"

    classifier = MongoFieldClassifier(CONNECTION_STRING, DATABASE_NAME)
    classifier.analyze_collection(COLLECTION_NAME)
    
    summary = classifier.get_classification_summary()
    print("Field Classification Summary:")
    print(f"Total Fields: {summary['total_fields']}")
    print("Dimensions:", summary['dimensions'])
    print("Metrics:", summary['metrics'])

if __name__ == "__main__":
    main()