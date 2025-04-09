from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.server_api import ServerApi


client = MongoClient(
    "mongodb+srv://komace:WAg6bn6QQDyPRxsd@cluster0.aklvj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)

db = client.book

# Створення документів
def create_documents():
    result_one = db.cats.insert_one(
        {
            "name": "barsik",
            "age": 3,
            "features": ["ходить в капці", "дає себе гладити", "рудий"],
        }
    )
    print(result_one.inserted_id)

    result_many = db.cats.insert_many(
        [
            {
                "name": "Lama",
                "age": 2,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Liza",
                "age": 4,
                "features": ["ходить в лоток", "дає себе гладити", "білий"],
            },
        ]
    )
    print(result_many.inserted_ids)

# Читання даних
def read_all():
    results = db.cats.find({})
    for el in results:
        print(el)

def read_by_name(name):
    result = db.cats.find_one({"name": name})
    print(result)

# Оновлення даних
def update_age_by_name(name, new_age):
    db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
    result = db.cats.find_one({"name": name})
    print(result)

def add_feature_by_name(name, feature):
    db.cats.update_one({"name": name}, {"$push": {"features": feature}})
    result = db.cats.find_one({"name": name})
    print(result)

# Видалення даних
def delete_by_name(name):
    db.cats.delete_one({"name": name})
    result = db.cats.find_one({"name": name})
    print(result)

def delete_all():
    db.cats.delete_many({})
    results = db.cats.find({})
    for el in results:
        print(el)

if __name__ == "__main__":
    create_documents()
    print("All documents:")
    read_all()

    print("\nDocument by name 'barsik':")
    read_by_name("barsik")

    print("\nUpdating age of 'barsik' to 4:")
    update_age_by_name("barsik", 4)

    print("\nAdding feature to 'barsik':")
    add_feature_by_name("barsik", "любить гратися")

    print("\nDeleting document by name 'barsik':")
    delete_by_name("barsik")

    print("\nDeleting all documents:")
    delete_all()
