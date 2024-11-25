import pymongo
import random
from nltk.corpus import words

# Ensure you have downloaded the NLTK words corpus
import nltk
nltk.download('words')

# MongoDB connection details
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["chatdb"]
collection = db["video-game-sales"]

# Function to get all fields in the collection
def get_collection_fields(collection):
    fields = set()
    for document in collection.find().limit(100):  # Limit to 100 documents for performance
        for key in document.keys():
            fields.add(key)
    return fields

# Function to get sample values for a field
def get_sample_values(collection, field, limit=10):
    values = set()
    for document in collection.find({}, {field: 1, "_id": 0}).limit(limit):
        if field in document:
            values.add(document[field])
    return list(values)

# Function to split fields into dimensions and metrics
def split_fields_into_dimensions_and_metrics(collection):
    dimensions = set()
    metrics = set()
    for document in collection.find().limit(100):
        for key, value in document.items():
            if isinstance(value, (int, float)):
                metrics.add(key)
            else:
                dimensions.add(key)
    return dimensions, metrics

# Function to generate a simple query pipeline
def generate_simple_query_pipeline(dimensions, metrics, collection):
    if dimensions:
        dim_field = random.choice(list(dimensions))
        dim_values = get_sample_values(collection, dim_field)
        dim_value = random.choice(dim_values) if dim_values else "default_value"
        return [{"$match": {dim_field: dim_value}}]
    else:
        return []

# Function to generate a medium complexity query pipeline
def generate_medium_query_pipeline(dimensions, metrics, collection):
    if dimensions and metrics:
        dim_field = random.choice(list(dimensions))
        dim_values = get_sample_values(collection, dim_field)
        dim_value = random.choice(dim_values) if dim_values else "default_value"

        metric_field = random.choice(list(metrics))
        metric_values = get_sample_values(collection, metric_field)
        metric_value = random.choice(metric_values) if metric_values else 0

        comparison = random.choice([("$gt", "greater than"), ("$lt", "less than")])
        return [{"$match": {dim_field: dim_value, metric_field: {comparison[0]: metric_value}}}]
    else:
        return []

# Function to generate a complex query pipeline with grouping and random sorting/limiting
def generate_complex_query_pipeline(dimensions, metrics, collection):
    if dimensions and metrics:
        dim_field = random.choice(list(dimensions))

        metric_field1 = random.choice(list(metrics))
        metric_field2 = random.choice(list(metrics))
        while metric_field2 == metric_field1:
            metric_field2 = random.choice(list(metrics))

        sort_field = random.choice([metric_field1, metric_field2])
        sort_order = random.choice([1, -1])
        include_limit = random.choice([True, False])
        if include_limit:
            limit_value = random.randint(5, 20)
            pipeline = [
                {
                    "$group": {
                        "_id": f"${dim_field}",
                        f"total_{metric_field1}": {"$sum": f"${metric_field1}"},
                        f"total_{metric_field2}": {"$sum": f"${metric_field2}"},
                        "count": {"$sum": 1}
                    }
                },
                {
                    "$sort": {f"total_{sort_field}": sort_order}
                },
                {
                    "$limit": limit_value
                }
            ]
        else:
            pipeline = [
                {
                    "$group": {
                        "_id": f"${dim_field}",
                        f"total_{metric_field1}": {"$sum": f"${metric_field1}"},
                        f"total_{metric_field2}": {"$sum": f"${metric_field2}"},
                        "count": {"$sum": 1}
                    }
                },
                {
                    "$sort": {f"total_{sort_field}": sort_order}
                }
            ]
        return pipeline
    else:
        return []

# # Get the fields from the collection
# fields = get_collection_fields(collection)

# Split fields into dimensions and metrics
dimensions, metrics = split_fields_into_dimensions_and_metrics(collection)

# Generate 3 sample query pipelines
simple_query_pipeline = generate_simple_query_pipeline(dimensions, metrics, collection)
medium_query_pipeline = generate_medium_query_pipeline(dimensions, metrics, collection)
complex_query_pipeline = generate_complex_query_pipeline(dimensions, metrics, collection)

# Print the generated query pipelines
print("Simple Query Pipeline:", simple_query_pipeline)
print("Medium Query Pipeline:", medium_query_pipeline)
print("Complex Query Pipeline:", complex_query_pipeline)

# # Example of running the pipelines
# print("\nResults of Simple Query Pipeline:")
# for doc in collection.aggregate(simple_query_pipeline):
#     print(doc)

# print("\nResults of Medium Query Pipeline:")
# for doc in collection.aggregate(medium_query_pipeline):
#     print(doc)

# print("\nResults of Complex Query Pipeline:")
# for doc in collection.aggregate(complex_query_pipeline):
#     print(doc)