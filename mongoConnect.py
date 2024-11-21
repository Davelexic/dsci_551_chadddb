from pymongo import MongoClient


def get_collection_fields(collection):
    ''' 
    Gets the fields from a sample document in the collection. \n
    Doesn't work on collections where every document has different fields. 
    '''
    
    sample_doc = collection.find_one()
    if sample_doc:
        return list(sample_doc.keys())
    else:
        return []  # Handle empty collections

def connect(url = 'mongodb://localhost:27017/'):
    return MongoClient(url)

def select_databse(client,dbName):
    if(client is None):
        # raise error
        print("Connect to mongo server before selecting database")
        return
    
    return client[dbName]

def list_collections(db):
    return db.list_collection_names()

def select_collection(db, collectionName):
    if(db is None):
        # raise error
        print("Select database before selecting collection")
        return

    return db[collectionName]

def close_connection(client):
    client.close()


# def main():
#     # connect to mongoDB
#     client = connect_to_db('mongodb://localhost:27017/')

#     # select database
#     db = select_databse(client, 'chatdb')

#     # get collection names
#     # allCollections = list_collections(db)

#     # select collection
#     collection = select_collection(db, 'video-game-sales')

#     print(get_collection_fields(collection))

#     # close connection
#     close_connection(client)

# main()


# get fields
# document = collection.find_one()
# if document:
#     field_names = document.keys()
#     print("Field names:", field_names)

# find
# for doc in collection.find({"Rank": 1}):
#     print(doc)