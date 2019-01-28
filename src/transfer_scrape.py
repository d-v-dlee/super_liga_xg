def scrape_to_list(scraped_rows, i, list_name):
    """insert row of rows of scraped data
    input i for skipping rows"""
    to_scrape = scraped_rows[i::7]
    list_name = []
    for i in range(len(to_scrape)):
        list_name.append(' '.join(to_scrape[i]))
    return list_name

def scrape_to_list_value(scraped_rows, i, list_name):
    """insert row of rows of scraped data
    input i for skipping rows
    return value in dollars"""
    to_scrape = scraped_rows[i::7]
    list_name = []
    for i in range(len(to_scrape)):
        num = float(to_scrape[i][0].replace(',', '.'))
        num_dollar = round((num * 1.14), 2)
        list_name.append(num_dollar)
    return list_name

def scrape_to_list_age_year(scraped_rows):
    """insert row of rows of scraped data
    return list of ages and years"""
    to_scrape = scraped_rows[3::7]
    ages= []
    years = []
    for i in range(len(to_scrape)):
        age = int(to_scrape[i][0])
        year_of_transfer = to_scrape[i][1]
        ages.append(age)
        years.append(year_of_transfer)
    return ages, years
