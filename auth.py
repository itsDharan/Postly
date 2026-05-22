# auth.py
import os
import certifi
import streamlit as st
from passlib.hash import pbkdf2_sha256
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from passlib.exc import InvalidHashError

# MongoDB connection — cached so it's not recreated on every Streamlit rerun
@st.cache_resource
def get_mongo_client():
    """Create and cache a single MongoDB client for the app lifetime."""
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    return MongoClient(
        uri,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
        socketTimeoutMS=30000,
    )

client = get_mongo_client()
db = client["linkedin_post_generator"]
users_collection = db["users"]
influencers_collection = db["influencers"]

INFLUENCERS = {
    "Influencer 1": "murlidharan",
    "Influencer 2": "khushburani",
    "Influencer 3": "ammaradil"
}

def init_db():
    """Initialize the database with influencers if not exists"""
    try:
        if not influencers_collection.count_documents({}):
            influencers_collection.insert_many([
                {"name": "Influencer 1", "username": "murlidharan", "dataset": "murli_data"},
                {"name": "Influencer 2", "username": "khushburani", "dataset": "khushbu_data"},
                {"name": "Influencer 3", "username": "ammaradil", "dataset": "ammar_data"}
            ])
    except PyMongoError as e:
        print(f"Warning: Could not initialize DB: {e}")

def register_user(username, password, influencer_username):
    """Register a new user with MongoDB"""
    try:
        # Check if username exists
        if users_collection.find_one({"username": username}):
            return False
        
        # Get influencer details
        influencer = influencers_collection.find_one({"username": influencer_username})
        if not influencer:
            return False
        
        # Create new user
        user_data = {
            "username": username,
            "password": pbkdf2_sha256.hash(password),
            "influencer": influencer_username,
            "influencer_name": influencer["name"],
            "dataset": influencer["dataset"]
        }
        
        users_collection.insert_one(user_data)
        return True
    except PyMongoError as e:
        print(f"Registration error: {e}")
        return False

def authenticate_user(username, password):
    """Authenticate user with MongoDB"""
    try:
        user = users_collection.find_one({"username": username})
        if not user:
            return False
        
        # Handle cases where password might not be properly hashed
        if not user.get("password"):
            return False
            
        try:
            return pbkdf2_sha256.verify(password, user["password"])
        except (ValueError, InvalidHashError):
            # Handle cases where the stored hash is invalid
            return False
    except PyMongoError as e:
        print(f"Auth error: {e}")
        return False

def get_user_data(username):
    """Get user data including influencer dataset"""
    try:
        return users_collection.find_one({"username": username}, {"_id": 0})
    except PyMongoError as e:
        print(f"Get user data error: {e}")
        return None

# Initialize the database on import
init_db()