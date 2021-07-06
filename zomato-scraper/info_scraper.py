import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh;'
                         ' Intel Mac OS X 10_15_4)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/83.0.4103.97 Safari/537.36'}


def get_info(url):
    """ Get Information about the restaurant from URL """
    
    global headers
    webpage = requests.get(url, headers=headers, timeout=3)
    html_text = BeautifulSoup(webpage.text, 'lxml')
    info = html_text.find_all('script', type='application/ld+json')[1]
    info = json.loads(info.string)
    
    data = (
        info['@type'], info['name'], info['url'], info['openingHours'],
        info['address']['streetAddress'], info['address']['addressLocality'],
        info['address']['addressRegion'], info['address']['postalCode'],
        info['address']['addressCountry'], 
        info['geo']['latitude'], info['geo']['longitude'],
        info['telephone'], info['priceRange'], info['paymentAccepted'],
        info['image'], info['servesCuisine'],
        info['aggregateRating']['ratingValue'], info['aggregateRating']['ratingCount']
    )
    return data


def save_df(file_name, df):
    """ Save the dataframe """
    
    df.to_csv(file_name, index=False)
    

def get_restaurant_info(url_list, save=True, file_name="Restaurants.csv"):
    """ Get Restaurant Information from all urls passed """

    # Collecting the data
    data = []
    for url in url_list:
        data.append(get_info(url))
        
    # Creating the DataFrame
    columns = ['Type', 'Name', 'URL', 'Opening_Hours',
               'Street', 'Locality', 'Region', 'PostalCode', 'Country',
               'Latitude', 'Longitude', 'Phone',
               'Price_Range', 'Payment_Methods',
               'Image_URL', 'Cuisine', 'Rating', 'Rating_Count']
    info_df = pd.DataFrame(data, columns=columns)
    
    # Save the df
    if save:
        save_df(file_name, info_df)
        
    return info_df


if __name__ == "__main__":
    urls = ["https://www.zomato.com/bangalore/voosh-thalis-bowls-1-bellandur-bangalore",
            "https://www.zomato.com/bangalore/flying-kombucha-itpl-main-road-whitefield-bangalore",
            "https://www.zomato.com/bangalore/matteo-coffea-indiranagar"]
    get_restaurant_info(urls)
