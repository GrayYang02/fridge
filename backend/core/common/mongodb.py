import mongoengine
import pymongo
from mongoengine import Document, StringField, BooleanField,IntField, DateTimeField,  BooleanField
from datetime import datetime
from fridgeserver.settings import MONGODB_DB,MONGODB_URI

mongoengine.connect( MONGODB_DB, host= MONGODB_URI )
# Connect to the MongoDB database
# Define the Food document
class UserRecipe(Document):
    id = StringField(required=True, primary_key=True)
    userid = IntField(required=True)
    recipe_id = IntField(required=True)
    op = StringField()
    create_time = DateTimeField(default=datetime.utcnow)
    update_time = DateTimeField(default=datetime.utcnow)
    is_del = BooleanField(default=False)



# Verify the inserted data
# print(f"Inserted food data: {food.to_json()}")
def getCollection(collect_name):
    client = pymongo.MongoClient( MONGODB_URI )
    db = client[ MONGODB_DB ]
    db_collection = db[collect_name]
    return db_collection

if __name__ == '__main__':
    recipe_db = getCollection('UserRecipe')
    documents = recipe_db.find()  # This will fetch all documents in the collection
    for document in documents:
        print(document)  # Print each document

    # insert data
    recipe = UserRecipe(
        id="1",  # Unique ID for the document
        userid=123,  # User ID
        recipe_id=456,  # Recipe ID
        op="create",  # Operation type (create, update, etc.)
        create_time=datetime.utcnow(),
        update_time=datetime.utcnow(),
        is_del=False  # Mark as not deleted
    )

    recipe.save()

    # insert index
    indexes = [
        ('create_time', pymongo.DESCENDING),
        ('update_time', pymongo.DESCENDING),
        ('recipe_id', pymongo.DESCENDING),
        ('userid', pymongo.DESCENDING),
        ('is_del', pymongo.DESCENDING)
    ]

    # Create indexes using a for loop
    for index in indexes:
        UserRecipe.create_index([index], background=True)
