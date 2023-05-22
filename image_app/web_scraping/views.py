from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from bs4 import BeautifulSoup
from config import AppCongiuration
from Logging.log_to_file import setup_logger


# Create your views here.
def web_scraping_view(request):
    if 'user_id' in request.session:
        app_initiate = AppCongiuration()
        app_config = app_initiate.load_app_config_settings()
        logger = setup_logger()
        page = requests.get('https://www.imdb.com/chart/top/')
        soup = BeautifulSoup(page.content, 'html.parser') 
        
        links = soup.select("table tbody tr td.titleColumn a") 
        movie_images = soup.select("table tbody tr td.posterColumn a img") 
        imdb_rating = soup.select("table tbody tr td.imdbRating strong") 
        list_movies = links[:15] 
        list_movies_rating = imdb_rating[:15] 
        list_movies_img = movie_images[:15]     
        anchor_list = []
        for index, element in enumerate(list_movies):            
            result = {
                'movie_title': element.text,
                'rating': list_movies_rating[index].text,
                'image_src': list_movies_img[index].get('src'),
            }
            anchor_list.append(result) 
        logger.info(app_config.web_scraping_imdb_success)
        return render(request,'web_scraping/scraping.html', {
            "movie_text" : anchor_list
        })
    else:
        redirect_path = reverse("logout")
        return HttpResponseRedirect(redirect_path)