from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from Movie_Scraping.scraping_service import MovieInfo
from Logging.log_to_file import setup_logger
from .models import Movies
from django.db.models import Q


# Create your views here.
def web_scraping_view(request):
    if 'user_id' in request.session:
        imdb_service = MovieInfo(1)
        imdb_movies_list = imdb_service.imdb_web_scraping()
        transaction_date = timezone.now()
        user_id = request.session['user_id']
        for idx, element in enumerate(imdb_movies_list):
            check_if_movie_exists = Movies.objects.filter(Q(movie_title__contains = element['movie_title']) & Q(movie_source__contains = 'imdb')).exists()
            if check_if_movie_exists is False:
                movies_db_save = Movies(movie_title = element['movie_title'], rating = element['rating'], 
                        movie_poster = element['image_src'], movie_source = 'imdb', 
                        created_by = user_id, created_date = transaction_date)
                movies_db_save.save()
        return render(request,'web_scraping/scraping.html', {
            "movie_text" : imdb_movies_list
        })
    else:
        redirect_path = reverse("logout")
        return HttpResponseRedirect(redirect_path)
    

def web_scraping_movie_site(request):
    if request.method == 'POST':
        try:
            logger = setup_logger()
            ott_type = request.POST.get('ott_type')
            movie_service = MovieInfo(int(ott_type))            
            if ott_type == '1':  
                movie_source = 'imdb'          
                web_movies_list = movie_service.imdb_web_scraping()
            else:
                movie_source = 'metacritic'  
                web_movies_list = movie_service.metacritic_web_scraping()
            transaction_date = timezone.now()
            user_id = request.session['user_id']
            for idx, element in enumerate(web_movies_list):
                check_if_movie_exists = Movies.objects.filter(Q(movie_title__contains = element['movie_title']) & Q(movie_source__contains = movie_source)).exists()
                if check_if_movie_exists is False:
                    movies_db_save = Movies(movie_title = element['movie_title'], rating = element['rating'], 
                          movie_poster = element['image_src'], movie_source = movie_source, 
                          created_by = user_id, created_date = transaction_date)
                    movies_db_save.save()
            return JsonResponse({"scraping_data": list(web_movies_list),  "responseCode": 200}, status=200, safe=False)               
        except Exception as ex:
            logger.error(f"Error occured while scraping movie sites Exception : {ex}")
            return JsonResponse({"message": ex, "responseCode": 400}, status=200)


