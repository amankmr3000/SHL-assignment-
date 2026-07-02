import urllib.request, os
url = os.getenv("CATALOG_URL", "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json")
os.makedirs("data", exist_ok=True)
urllib.request.urlretrieve(url, "data/catalog.json")
print("saved data/catalog.json")
