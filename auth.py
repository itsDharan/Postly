# auth.py
import os
import ssl
import certifi
import streamlit as st
from passlib.hash import pbkdf2_sha256
from pymongo import MongoClient
from pymongo.errors import PyMongoError

try:
    from passlib.exc import InvalidHashError
except ImportError:
    InvalidHashError = ValueError

# MongoDB connection — cached so it's not recreated on every Streamlit rerun
@st.cache_resource
def get_mongo_client():
    """Create and cache a single MongoDB client for the app lifetime."""
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

    # Append TLS params to URI if not already present
    separator = "&" if "?" in uri else "?"
    if "tls=" not in uri.lower():
        uri += f"{separator}tls=true&tlsAllowInvalidCertificates=true"

    return MongoClient(
        uri,
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

def check_db_connection():
    """Check if MongoDB is connected. Returns (ok, message)."""
    try:
        client.admin.command('ping')
        inf_count = influencers_collection.count_documents({})
        usr_count = users_collection.count_documents({})
        return True, f"Connected. Influencers: {inf_count}, Users: {usr_count}"
    except Exception as e:
        return False, f"DB Error: {type(e).__name__}: {e}"

def init_db():
    """Initialize the database with influencers if not exists"""
    try:
        if not influencers_collection.count_documents({}):
            influencers_collection.insert_many([
                {"name": "Influencer 1", "username": "murlidharan", "dataset": "murli_data"},
                {"name": "Influencer 2", "username": "khushburani", "dataset": "khushbu_data"},
                {"name": "Influencer 3", "username": "ammaradil", "dataset": "ammar_data"}
            ])
    except PyMongoError:
        pass

def register_user(username, password, influencer_username):
    """Register a new user with MongoDB. Returns (success, error_message)."""
    try:
        if users_collection.find_one({"username": username}):
            return False, "Username already exists"

        influencer = influencers_collection.find_one({"username": influencer_username})
        if not influencer:
            return False, f"Influencer '{influencer_username}' not found in database"

        user_data = {
            "username": username,
            "password": pbkdf2_sha256.hash(password),
            "influencer": influencer_username,
            "influencer_name": influencer["name"],
            "dataset": influencer["dataset"]
        }

        users_collection.insert_one(user_data)
        return True, "Success"
    except PyMongoError as e:
        return False, f"Database error: {type(e).__name__}: {e}"

def authenticate_user(username, password):
    """Authenticate user. Returns (success, error_message)."""
    try:
        user = users_collection.find_one({"username": username})
        if not user:
            return False, "User not found"

        if not user.get("password"):
            return False, "No password stored for user"

        try:
            if pbkdf2_sha256.verify(password, user["password"]):
                return True, "Success"
            else:
                return False, "Wrong password"
        except (ValueError, InvalidHashError) as e:
            return False, f"Password hash error: {e}"
    except PyMongoError as e:
        return False, f"Database error: {type(e).__name__}: {e}"

def get_user_data(username):
    """Get user data including influencer dataset."""
    try:
        return users_collection.find_one({"username": username}, {"_id": 0})
    except PyMongoError:
        return None

# Initialize the database on import
init_db()