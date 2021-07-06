import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh;'
                         ' Intel Mac OS X 10_15_4)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/83.0.4103.97 Safari/537.36'}


def get_description(html_text):
    """ Gets the Menu Item along with Description and Category """
    
    menu = html_text.find_all('script', type='application/ld+json')[3]
    menu = json.loads(menu.string)
    data = []
    for section in menu['hasMenuSection']:
        name = section['name']
        if name == "Recommended":
            continue
        menu_items = section['hasMenuSection'][0]['hasMenuItem']
        for item in menu_items:
            data.append((
                item['name'],
                item['description'],
                name,
            ))

    # Creating the dataframe
    columns = ['Name', 'Description', 'Category']
    return pd.DataFrame(data, columns=columns)


def get_price_tags(html_text):
    """ Gets the Menu Item along with Price and Tags """
    
    menu_items = [div for div in html_text.find_all('div') if div.find('h4', recursive=False)]
    data = []
    for item in menu_items:
        item = item.find_all(text=True)
        name = item[0]
        price = item[-1].replace("₹", "Rs ")
        tags = ", ".join(item[1:-1])
        data.append((name, price, tags))

    # Creating the dataframe
    columns = ['Name', 'Price', 'Tags']
    df = pd.DataFrame(data, columns=columns)
    df = df[~df.duplicated(['Name'])]
    df = df.reset_index().drop(columns='index')
    return df


def save_df(name, df):
    """ Save the dataframe """
    
    if not os.path.exists("Menu"):
        os.makedirs("Menu")
    df.to_csv(f"Menu/{name}.csv", index=False)


def get_menu(url, save=True):
    """ Get all Menu Items from the passed url """
    
    global headers
    url += '/order'
    
    # Request for the webpage
    webpage = requests.get(url, headers=headers, timeout=5)
    html_text = BeautifulSoup(webpage.text, 'lxml')
    restaurant_name = html_text.head.find('title').text[:-22]
    
    # Collecting the data
    df1 = get_description(html_text)
    df2 = get_price_tags(html_text)
    menu_df = df1.merge(df2, on='Name')
    
    # Save the df
    if save:
        save_df(restaurant_name, menu_df)
    return menu_df


if __name__ == "__main__":
    link = "https://www.zomato.com/bangalore/voosh-thalis-bowls-1-bellandur-bangalore"
    dframe = get_menu(link, save=True)
