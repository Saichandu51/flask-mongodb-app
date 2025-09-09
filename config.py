import os
from dotenv import load_dotenv

load_dotenv()

# Replace these values with your actual MongoDB Atlas details
MONGODB_URI = os.getenv('MONGODB_URI', 'your_actual_connection_string_here')
DB_NAME = os.getenv('DB_NAME', 'myflaskapp')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'submissions')
