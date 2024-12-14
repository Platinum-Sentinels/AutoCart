from tavily import TavilyClient
from dotenv import load_dotenv
import os
load_dotenv()

# Step 1. Instantiating your TavilyClient
tavily_client = TavilyClient(os.getenv('TRAVITY_KEY'))

# Step 2. Executing a simple search query
response = tavily_client.search("What are the best asus rog laptop deals in online store  named amazon and ebay give me few")

# Step 3. That's it! You've done a Tavily Search!
for i in response['results']:
    print(i,"\n")