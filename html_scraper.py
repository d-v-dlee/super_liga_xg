# Setup MongoDB connection to MongoDB collection

import urllib.request, json 
import pymongo
import time

mc = pymongo.MongoClient()
db = mc['gameinfo_db']
coll = db['games']
players = db['players']

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


#dropped games from mongoDB = [448694, 448698, 448623, 448627, 448633, 448679]

def scrape_player_info(urls, delay=15):
    """Return a dictionary of dictionary of data from a table.
    
    Arguments
    ---------
    url : str
        The URL of the site to scrape.
    """
    chars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'k', 'm', '.']
    time.sleep(delay)
    for url in urls:
        club = url.split('/')[3]
        browser.get(url)
        player_dict_odd = {}
        for row in browser.find_elements_by_css_selector("tr.odd"):
            player = row.find_element_by_css_selector('td.hauptlink a').text
            squad_num = row.find_elements_by_css_selector('td.zentriert')[0].text
            birthday = row.find_elements_by_css_selector('td.zentriert')[1].text
            transfer_value = row.find_element_by_css_selector('td.rechts.hauptlink').text.strip()
            player_dict_odd[player] = {'club': club, 'squad_num': squad_num, 'birthday': birthday, 'transfer_value(sterlings)': transfer_value}
        player_dict_even = {}
        for row in browser.find_elements_by_css_selector("tr.even"):
            player = row.find_element_by_css_selector('td.hauptlink a').text
            squad_num = row.find_elements_by_css_selector('td.zentriert')[0].text
            birthday = row.find_elements_by_css_selector('td.zentriert')[1].text
        #     nationality = row.find_element_by_css_selector('td.zentriert.img')
            transfer_value = row.find_element_by_css_selector('td.rechts.hauptlink').text.strip()
            player_dict_even[player] = {'club': club, 'squad_num': squad_num, 'birthday': birthday, 'transfer_value(sterlings)': transfer_value}
        player_dict = {**player_dict_even, **player_dict_odd}
        db.players.insert_one(player_dict)


    
