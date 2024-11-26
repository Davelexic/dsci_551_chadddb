import re
from pymongo import MongoClient
import json
from bson import json_util

# Map English to MongoDB operators
OPERATORS_MAP = {
    "greater than": "$gt",
    "more than": "$gt",
    "less than": "$lt",
    "lesser than": "$lt",
    "equal to": "$eq",
    "not equal to": "$ne",
}

def parse_query(english_query: str):
    """
    Parse plain English query to extract collection, field, condition, and value.
    """
    # Example pattern matching: "Find all <collection> where <field> <condition> <value>"
    match = re.match(r"Find all ([\w\-]+) where (\w+) (.+) (\d+)", english_query)
    if not match:
        raise ValueError("Invalid query format.")

    collection, field, condition, value = match.groups()
    return collection, field, condition, int(value)


def build_pipeline(field, condition, value):
    """
    Build MongoDB aggregation pipeline from parsed components.
    """
    operator = OPERATORS_MAP.get(condition)
    if not operator:
        raise ValueError(f"Unsupported condition: {condition}")

    return [{"$match": {field: {operator: value}}}]


def execute_pipeline(collection_name, pipeline):
    """
    Execute pipeline using PyMongo.
    """
    client = MongoClient("mongodb://localhost:27017")
    db = client["chatdb"]  # Replace with your database name
    collection = db[collection_name]
    results = list(collection.aggregate(pipeline))
    # return json.dumps(results, default=json_util.default)
    return results,pipeline


# # Main application
# if __name__ == "__main__":
#     english_query = "Find all video-game-sales where Global_Sales greater than 82.5"
#     try:
#         collection, field, condition, value = parse_query(english_query)
#         pipeline = build_pipeline(field, condition, value)
#         print(pipeline,collection)
#         results = execute_pipeline(collection, pipeline)
#         print("Results:", results)
#     except Exception as e:
#         print(f"Error: {e}")