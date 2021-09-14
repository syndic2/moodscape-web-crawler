from extensions import mongo

def get_sequence(collection):
    is_collection_exist_query= { '_id': collection }
    document= mongo.sequences.find_one(is_collection_exist_query)

    if document is None:
        mongo.sequences.insert_one({ '_id': collection, 'value': 0 })

    document= mongo.sequences.find_one_and_update(is_collection_exist_query, { '$inc': { 'value': 1 } }, return_document= True)

    return document['value']