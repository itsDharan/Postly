from pymongo import MongoClient

# Connect to MongoDB (default URI for local)
client = MongoClient("mongodb://localhost:27017/")

# Create/Get the database
db = client["influencer_database"]

# Sample data for each collection
murli_data = [
    {"name": "Murli Sharma", "followers": 12000, "platform": "Instagram"},
    {"name": "Murli Blog", "followers": 8000, "platform": "YouTube"}
]

khushbu_data = [
    {"name": "Khushbu Patel", "followers": 20000, "platform": "Instagram"},
    {"name": "Khushbu's Kitchen", "followers": 15000, "platform": "YouTube"}
]

ammar_data = [
    {"name": "Ammar Ali", "followers": 18000, "platform": "TikTok"},
    {"name": "Ammar Fitness", "followers": 10000, "platform": "Instagram"}
]

# Insert data into respective collections
db["murli_data"].insert_many(murli_data)
db["khushbu_data"].insert_many(khushbu_data)
db["ammar_data"].insert_many(ammar_data)

print("Data successfully inserted into MongoDB!")
