"""
seed.py — Populate MongoDB with post datasets and influencer metadata.

Usage:
    python seed.py                          # uses MONGO_URI env var, falls back to localhost
    MONGO_URI="mongodb+srv://..." python seed.py   # seed a remote Atlas cluster
"""

import json
import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["linkedin_post_generator"]

# Mapping: JSON file in Data/ → MongoDB collection name
DATASET_MAP = {
    "Data/Murli_Data.json": "murli_data",
    "Data/Khushbu_data.json": "khushbu_data",
    "Data/Adil_Data.json": "ammar_data",
}

# Influencer metadata (must match auth.py INFLUENCERS dict)
INFLUENCERS = [
    {"name": "Influencer 1", "username": "murlidharan", "dataset": "murli_data"},
    {"name": "Influencer 2", "username": "khushburani", "dataset": "khushbu_data"},
    {"name": "Influencer 3", "username": "ammaradil", "dataset": "ammar_data"},
]


def seed_posts():
    """Load JSON files and insert into their respective collections."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for filepath, collection_name in DATASET_MAP.items():
        full_path = os.path.join(base_dir, filepath)
        if not os.path.exists(full_path):
            print(f"⚠  File not found, skipping: {full_path}")
            continue

        with open(full_path, encoding="utf-8") as f:
            posts = json.load(f)

        collection = db[collection_name]
        collection.drop()  # clear old data to avoid duplicates
        collection.insert_many(posts)
        print(f"✅ Inserted {len(posts)} posts into '{collection_name}'")


def seed_influencers():
    """Ensure the influencers collection exists."""
    col = db["influencers"]
    col.drop()
    col.insert_many(INFLUENCERS)
    print(f"✅ Inserted {len(INFLUENCERS)} influencer records")


if __name__ == "__main__":
    print(f"Connecting to: {MONGO_URI}")
    seed_posts()
    seed_influencers()
    print("\n🎉 Seeding complete!")
