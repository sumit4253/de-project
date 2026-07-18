import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

def get_db():
    """Establish and return a MongoDB database instance."""
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    db_name = os.environ.get('DB_NAME', 'smart_irrigator')
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Force a connection test
        client.admin.command('ping')
        return client[db_name]
    except ConnectionFailure as e:
        print(f"Error while connecting to MongoDB: {e}")
        return None

def init_db():
    """Initialize collections and insert default crops."""
    db = get_db()
    if db is None:
        print("Failed to initialize database: Cannot connect to MongoDB.")
        return
        
    # Insert default crops if the collection is empty
    if db.crops.count_documents({}) == 0:
        default_crops = [
            {'name': 'Wheat', 'min_temp': 10, 'max_temp': 25, 'min_humidity': 40, 'max_humidity': 70, 'base_water_req': 400, 'season': 'Winter'},
            {'name': 'Rice', 'min_temp': 20, 'max_temp': 35, 'min_humidity': 60, 'max_humidity': 90, 'base_water_req': 900, 'season': 'Monsoon'},
            {'name': 'Cotton', 'min_temp': 21, 'max_temp': 30, 'min_humidity': 50, 'max_humidity': 80, 'base_water_req': 700, 'season': 'Summer'},
            {'name': 'Sugarcane', 'min_temp': 20, 'max_temp': 35, 'min_humidity': 70, 'max_humidity': 95, 'base_water_req': 1500, 'season': 'All'},
            {'name': 'Maize', 'min_temp': 18, 'max_temp': 27, 'min_humidity': 50, 'max_humidity': 75, 'base_water_req': 500, 'season': 'Monsoon'}
        ]
        db.crops.insert_many(default_crops)
        print("Default crops inserted.")
        
    print("MongoDB database initialized successfully.")

if __name__ == '__main__':
    init_db()
