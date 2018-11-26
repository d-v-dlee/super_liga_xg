# Setup MongoDB connection to MongoDB collection

import urllib.request, json 
import pymongo
import time

mc = pymongo.MongoClient()
db = mc['gameinfo_db']
coll = db['games']

def get_urls(page_links):
    """Insert page links, return list of url addresses of the json"""
    urls = []
    for link in page_links:
        link1 = link.replace('v3', 'VV')
        game_id = ''.join([char for char in link1 if char in list(map(str, list(range(10))))])
        json_url = f'http://www.afa.com.ar/deposito/html/v3/htmlCenter/data/deportes/futbol/primeraa/events/{game_id}.json'
        urls.append(json_url)
    return urls

# def insert_new_games(game_urls):
#     """Insert game only if their URLs aren't already in the DB"""
#     for game in game_urls:
#         if coll.count_documents({'url': coll['url']}) == 0:
#             coll.insert_one(game)

def scrape_soccer_json(urls):
    """
    Makes a request to AFA's website and retrieves the 
    soccer data in JSON format.
    Dumps the JSON response into mongodb.
    Parameters
    ----------
    urls: list of strings which are url addresses
    
    Returns
    -------
    None
    """
    for url in urls:
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            coll.insert_one(data)
            time.sleep(15)