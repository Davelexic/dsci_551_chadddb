# query generator
import mongoConnect

clauses = {
    'limit': {'$limit': 10},
    'match': {'$match': {}} 
}
pipeline = []

pipelines = [
    [
        {'$limit': 10}
    ],
    [
        {'$match' : {'Genre':'Platform'}}
    ],
    [
        {
            '$group' : {
                '_id': '$Year',
                'TotalNASales': { '$sum': "$NA_Sales" },
                'TotalEUSales': { '$sum': "$EU_Sales" },
                'TotalJPSales': { '$sum': "$JP_Sales" }
            }
        }
    ]
]

def create_pipeline():
    # default:
    pipeline.append(clauses['limit'])
    match_clause = clauses['match']
    match_clause['$match'] = {
        'Genre': 'Platform'
    }
    pipeline.append(match_clause)

def main():
    client = mongoConnect.connect()
    db = mongoConnect.select_databse(client,'chatdb')
    collection = mongoConnect.select_collection(db,'video-game-sales')
    # create_pipeline()
    # print(pipeline)
    print(list(collection.aggregate(pipelines[2])))

main()