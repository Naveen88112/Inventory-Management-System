from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get MongoDB URI from environment variable
uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(uri)

# Choose your DB and collections
db = client["inventory_db"]
product_collection = db["products"]
customer_collection = db["customers"]
premium_customer_collection = db["premium_customers"]
sale_collection = db["sales"]

print("✅ MongoDB connected successfully!")

