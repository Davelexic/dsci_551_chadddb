import nltk
import spacy
import re

# Download necessary NLTK resources if you haven't already
nltk.download('punkt')
nltk.download('wordnet')

# Load spaCy's English language model
nlp = spacy.load("en_core_web_sm")


def english_to_nosql(english_query):
    """Converts plain English input to a NoSQL query (MongoDB style)."""

    # 1. Tokenization and Lemmatization
    doc = nlp(english_query)
    lemmatized_tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]

    # 2. Pattern Matching and Query Construction
    query = {}
    collection = None  # Initialize the collection name

    # Example patterns (expand these as needed)
    patterns = {
        "find all": lambda: {},  # Empty query to retrieve all documents
        "find where": lambda field, value: {field: value},
        "find with": lambda field, value: {field: value},  # Synonym for "find where"
        "greater than": lambda field, value: {field: {"$gt": float(value)}},  # Handle numerical comparisons
        "less than": lambda field, value: {field: {"$lt": float(value)}},
        "equal to": lambda field, value: {field: value},
        "in collection": lambda coll_name: setattr(collection, coll_name, coll_name),  # To specify the collection
    }

    i = 0
    while i < len(lemmatized_tokens):
        token = lemmatized_tokens[i]

        for pattern, action in patterns.items():
            if " ".join(lemmatized_tokens[i:i + len(pattern.split())]) == pattern:


                if pattern == "find all":
                    query = {}  # Return all documents
                    i += len(pattern.split())
                    break

                elif pattern in ["find where", "find with", "equal to"]:
                    field = lemmatized_tokens[i + len(pattern.split())]
                    value = lemmatized_tokens[i + len(pattern.split()) + 2]  # Assuming "is" or similar in between
                    try:  # Attempt numeric conversion
                        value = float(value)
                    except ValueError:
                        pass # Keep as string if not a number
                    query.update(action(field, value))
                    i += len(pattern.split()) + 3  # Skip field, value, and connecting word
                    break
                elif pattern in ["greater than", "less than"]:
                     field = lemmatized_tokens[i + len(pattern.split())]
                     value = lemmatized_tokens[i + len(pattern.split()) + 1]
                     query.update(action(field, value))  # Update the main query
                     i += len(pattern.split()) + 2
                     break



                elif pattern == "in collection":
                    coll_name = lemmatized_tokens[i + len(pattern.split())]
                    collection = coll_name  # Set the collection name
                    i += len(pattern.split()) + 1  # Skip the collection name
                    break
        else:
            i += 1  # Move to the next token if no pattern matches

    return {"collection": collection, "query": query}  # Return both query and collection




# Example usage:
english_queries = [
    "Find all documents in collection users",
    "Find where age is greater than 25",
    "Find with city equal to London",
    "find where name is John in collection products"
]


for english_query in english_queries:
    nosql_query = english_to_nosql(english_query)
    print(f"English: {english_query}")
    print(f"NoSQL: {nosql_query}")
    print("-" * 20)