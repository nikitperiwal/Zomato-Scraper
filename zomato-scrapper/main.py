from info_scrapper import get_restaurant_info
from review_scrapper import get_reviews
from menu_scrapper import get_menu


def scrape_all_data(url_list):
    """Scrapes all data from the urls passed """

    get_restaurant_info(url_list=url_list, file_name="Restaurants.csv")
    for url in url_list:
        get_reviews(url=url, max_reviews=50, sort="popular", save=True)
        get_menu(url)


if __name__ == '__main__':
    urls = ["https://www.zomato.com/bangalore/voosh-thalis-bowls-1-bellandur-bangalore",
            "https://www.zomato.com/bangalore/flying-kombucha-itpl-main-road-whitefield-bangalore",
            "https://www.zomato.com/bangalore/matteo-coffea-indiranagar"]
    scrape_all_data(urls)
