# few_shot.py
import os
import certifi
import pandas as pd
from pymongo import MongoClient

class FewShotPosts:
    def __init__(self, dataset_name):
        self.client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"), tlsCAFile=certifi.where())
        self.db = self.client["linkedin_post_generator"]
        self.dataset_name = dataset_name
        self.df = None
        self.unique_tags = None
        self.load_posts()

    def load_posts(self):
        """Load posts from MongoDB based on the dataset name"""
        collection = self.db[self.dataset_name]
        posts = list(collection.find({}, {'_id': 0}))
        
        if posts:
            self.df = pd.json_normalize(posts)
            self.df['length'] = self.df['line_count'].apply(self.categorize_length)
            all_tags = self.df['tags'].apply(lambda x: x).sum()
            self.unique_tags = list(set(all_tags))
        else:
            # Fallback to empty DataFrame if no data
            self.df = pd.DataFrame()
            self.unique_tags = []

    # ... rest of the class remains the same ...
    def get_filtered_posts(self, length, language, tag):
        if self.df.empty:
            return []
            
        df_filtered = self.df[
            (self.df['tags'].apply(lambda tags: tag in tags)) &
            (self.df['language'] == language) &
            (self.df['length'] == length)
        ]
        return df_filtered.to_dict(orient='records')

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags

    def __del__(self):
        self.client.close()