# Setup MongoDB connection to MongoDB collection
from selenium.webdriver import (Chrome, Firefox)
import time

import requests
from bs4 import BeautifulSoup


import urllib.request, json 
import pymongo
import time

mc = pymongo.MongoClient()
db = mc['gameinfo_db']
coll = db['games']
players = db['players']
teams = db['teams']

#turned off because scrape complete...
# browser = Firefox()


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

raw_html_coll = db['raw_html']

def scrape_page(url):
    """Get the HTML source from url and cache it. Check cache for existing results before scraping."""
    found_html = raw_html_coll.find_one({'url': url})
    if found_html:
        page_source = found_html['page_source']
    else:
        browser.get(url)
        time.sleep(5)
        page_source = browser.page_source
        raw_html_coll.insert_one({'url': url, 'page_source': page_source})
    return page_source


def get_player_data(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    club = soup.select_one('div.table-header').text.strip()
    for row in soup.select('tr.odd'):
        yield parse_row(row, club)
    for row in soup.select('tr.even'):
        yield parse_row(row, club)


def parse_row(row, club):
    """Return the values from a row element as a dictionary."""
    player = row.select_one('td.hauptlink a').text
    squad_num = row.select('td.zentriert')[0].text
    birthday = row.select('td.zentriert')[1].text
    height = row.select('td.zentriert')[3].text
    foot = row.select('td.zentriert')[4].text
    transfer_value = row.select_one('td.rechts.hauptlink').text.strip()
    player_dict = {
        'player': player,
        'club': club,
        'squad_num': squad_num,
        'height': height,
        'foot': foot,
        'birthday': birthday,
        'transfer_value(sterlings)': transfer_value
    }
    return player_dict


def get_all_player_data_from_url(url):
    page_source = scrape_page(url)
    yield from get_player_data(page_source)


# def team_scrape(urls):
#     for url in urls:
#         db.teams.insert_one(get_all_player_data_from_url(url))

def add_player_to_db(player_dict):
    """remove any duplicates and add player"""
    player = player_dict['player']
    club = player_dict['club']
    players.delete_many({'player': player, 'club': club})
    players.insert_one(player_dict)



# def scrape_player_info(urls, delay=15):
#     """Return a dictionary of dictionary of data from a table.
    
#     Arguments
#     ---------
#     url : str
#         The URL of the site to scrape.
#     """
#     chars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'k', 'm', '.']
#     for url in urls:
#         time.sleep(delay)
#         club = url.split('/')[3]
#         browser.get(url)
#         player_dict_odd = {}
#         for row in browser.find_elements_by_css_selector("tr.odd"):
#             player = row.find_element_by_css_selector('td.hauptlink a').text
#             squad_num = row.find_elements_by_css_selector('td.zentriert')[0].text
#             birthday = row.find_elements_by_css_selector('td.zentriert')[1].text
#             transfer_value = row.find_element_by_css_selector('td.rechts.hauptlink').text.strip()
#             player_dict_odd[player] = {'club': club, 'squad_num': squad_num, 'birthday': birthday, 'transfer_value(sterlings)': transfer_value}
#         player_dict_even = {}
#         for row in browser.find_elements_by_css_selector("tr.even"):
#             player = row.find_element_by_css_selector('td.hauptlink a').text
#             squad_num = row.find_elements_by_css_selector('td.zentriert')[0].text
#             birthday = row.find_elements_by_css_selector('td.zentriert')[1].text
#         #     nationality = row.find_element_by_css_selector('td.zentriert.img')
#             transfer_value = row.find_element_by_css_selector('td.rechts.hauptlink').text.strip()
#             player_dict_even[player] = {'club': club, 'squad_num': squad_num, 'birthday': birthday, 'transfer_value(sterlings)': transfer_value}
#         player_dict = {**player_dict_even, **player_dict_odd}
#         db.players.insert_one(player_dict)
            




    
