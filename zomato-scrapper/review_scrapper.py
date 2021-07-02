import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh;'
                         ' Intel Mac OS X 10_15_4)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/83.0.4103.97 Safari/537.36'}


def clean_reviews(html_text):
    """ Cleans and collect the review from the html """
    
    reviews = html_text.find_all('script', type='application/ld+json')[1]
    reviews = json.loads(reviews.string)['reviews']
    data = []
    for review in reviews:
        data.append((
            review['author'],
            review['url'],
            review['description'],
            review['reviewRating']['ratingValue']
        ))
    return data


def save_df(name, df):
    """ Save the dataframe """
    
    if not os.path.exists("Reviews"):
        os.makedirs("Reviews")
    df.to_csv(f"Reviews/{name}.csv", index=False)


def get_reviews(url, max_reviews, sort='popular', save=True):
    """ Get all Reviews from the passed url """
    
    global headers
    
    # Setiing variables for the scraping
    max_reviews = max_reviews//5
    if sort == 'popular':
        sort = '&sort=rd'
    elif sort == 'new':
        sort = '&sort=dd'
    
    reviews = []
    prev_data = None
    rn = ""

    # Collecting the reviews
    for i in range(1, max_reviews):
        link = url+f"/reviews?page={i}{sort}"
        webpage = requests.get(link, headers=headers, timeout=5)
        html_text = BeautifulSoup(webpage.text, 'lxml')
        rn = html_text.head.find('title').text
        data = clean_reviews(html_text)
        if prev_data == data:
            break
        reviews.extend(data)
        prev_data = data
    
    # Creating the DataFrame
    restaurant_name = rn[rn.find("User Reviews"):-1]
    columns = ['Author', 'Review URL', 'Description', 'Rating']
    review_df = pd.DataFrame(reviews, columns=columns)
    
    # Saving the df
    if save:
        save_df(restaurant_name, review_df)
    
    return review_df


if __name__ == "__main__":
    get_reviews("https://www.zomato.com/bangalore/meghana-foods-marathahalli-bangalore", 70, sort='new')
