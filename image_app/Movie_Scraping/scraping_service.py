from config import AppCongiuration
from Movie_Scraping.scraping_abc import WebScraping
import requests
from bs4 import BeautifulSoup
from Logging.log_to_file import setup_logger


class MovieInfo(WebScraping):
    def __init__(self, ott_type):
        app_initiate = AppCongiuration()
        self.app_config = app_initiate.load_app_config_settings()
        self.logger = setup_logger()
        self.ott_type = ott_type

    def imdb_web_scraping(self):
        session = requests.Session()
        session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        page = session.get(self.app_config.imdb_movie_site, allow_redirects=True)
        soup = BeautifulSoup(page.content, 'html.parser')    
        links = soup.select("table tbody tr td.titleColumn a") 
        movie_images = soup.select("table tbody tr td.posterColumn a img") 
        imdb_rating = soup.select("table tbody tr td.imdbRating strong") 
        list_movies = links[:10] 
        list_movies_rating = imdb_rating[:10] 
        list_movies_img = movie_images[:10]     
        top10_movies_list = []
        for index, element in enumerate(list_movies):            
            result = {
                'movie_title': element.text,
                'rating': list_movies_rating[index].text,
                'image_src': list_movies_img[index].get('src'),
            }
            top10_movies_list.append(result)   
        self.logger.info(self.app_config.web_scraping_imdb)
        return top10_movies_list


    def metacritic_web_scraping(self):
        session = requests.Session()
        session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        if self.ott_type == 2:
            page = session.get(self.app_config.meta_critic_netflix, allow_redirects=True)
        elif self.ott_type == 3:
            page = session.get(self.app_config.meta_critic_piv, allow_redirects=True)
        else:
            page = session.get(self.app_config.meta_critic_hulu, allow_redirects=True)
        soup = BeautifulSoup(page.content, 'html.parser') 
        links = soup.select(".clamp-summary-wrap a h3")
        movie_images = soup.select(".clamp-image-wrap a img")
        imdb_rating = soup.select(".clamp-score-wrap a div")
        list_movies = links[:10] 
        list_movies_rating = imdb_rating[:10] 
        list_movies_img = movie_images[:10]     
        top10_movies_list = []
        for index, element in enumerate(list_movies):            
            result = {
                'movie_title': element.text,
                'rating': list_movies_rating[index].text,
                'image_src': list_movies_img[index].get('src'),
            }
            top10_movies_list.append(result)   
        self.logger.info(self.app_config.web_scraping_metacritic)
        return top10_movies_list

    