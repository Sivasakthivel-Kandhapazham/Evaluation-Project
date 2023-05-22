from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, Http404
from .models import Category, ImageGallery
from login.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.core.files.uploadedfile import UploadedFile
import base64
import numpy as np
from image_app.email_service import send_email
from config import AppCongiuration
from Logging.log_to_file import setup_logger


# Create your views here.
def logout(request):
     request.session.flush()
     return render(request,'login/login.html')


def image_gallery_view(request):
    if 'user_id' in request.session:
        category_list = Category.objects.all()
        image_gallery = ImageGallery.objects.all()
        return render(request,'imaging_hub/image_gallery.html', {
            "categorys": category_list,
            "images": image_gallery
        })
    else:
        redirect_path = reverse("logout")
        return HttpResponseRedirect(redirect_path)


def image_upload_view(request):
    if 'user_id' in request.session:
        category_list = Category.objects.all()
        return render(request,'imaging_hub/image_upload.html', {
            "categorys": category_list
        })
    else:
        redirect_path = reverse("logout")
        return HttpResponseRedirect(redirect_path)


def upload_image_process(request):
    if request.method == 'POST':
        try:         
            image_file = request.FILES.get("image")  
            app_initiate = AppCongiuration()
            app_config = app_initiate.load_app_config_settings()
            logger = setup_logger()
            if image_file is None:
                logger.info(app_config.image_empty_msg)
                return JsonResponse({"message": app_config.image_empty_msg , "responseCode": 220}, status=200)
            
            extension = image_file.name.split('.')[-1]   
            if not extension or extension.lower() not in app_config.image_file_types:
                 logger.info(app_config.image_extension_msg)
                 return JsonResponse({"message": app_config.image_extension_msg , "responseCode": 220}, status=200)         
                   
            if image_file.size > app_config.image_file_size:
                 logger.info(f'{app_config.image_size_error_message} {np.round(image_file.size/1048576,0)} MB')
                 return JsonResponse({"message": f'{app_config.image_size_error_message} {np.round(image_file.size/1048576,0)} MB', "responseCode": 220}, status=200)
            
            title = request.POST.get('title')
            description = request.POST.get('description')
            category_type = request.POST.get('category_type')
            category_model = Category.objects.get(pk = int(category_type))
            transaction_date = timezone.now()
            if isinstance(image_file, UploadedFile):
                binary_data = image_file.read()
            else:
                binary_data = None 
            image_gallery = ImageGallery(image  = image_file, title = title, description = description, 
                                    category_type = category_model, created_by = request.session['user_id'],
                                    created_date = transaction_date, image_data = binary_data)
            image_gallery.save()
            send_email(f"Image with name {image_file.name} uploaded successfully", "Success - Image uploaded")
            return JsonResponse({"message": "Image upload successful", "responseCode": 200}, status=200)
        except Exception as ex:
            logger.error(f"Error occured while uploading image with name {image_file.name} exception : {ex}")
            send_email(f"Error occured while uploading image with name {image_file.name}", "Failure - Image uploaded!")
            return JsonResponse({"message": ex, "responseCode": 400}, status=200)
     

def image_detailed_view(request, id):
    try:
        if 'user_id' in request.session:
            image_gallery = ImageGallery.objects.get(pk=id)
            user_name = User.objects.get(id = image_gallery.created_by)  
            full_name = f'{user_name.firstname} {user_name.lastname}'
            return render(request, "imaging_hub/image_view.html", {
                "title": image_gallery.title,
                "description": image_gallery.description,
                "category": image_gallery.category_type.category_type,
                "uploaded_by": full_name,
                "image_binary_data": image_gallery.image_data,
            })
        else:
            redirect_path = reverse("logout")
            return HttpResponseRedirect(redirect_path)
    except:
        raise Http404


def image_gallery_filter(request):     
     try:
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_type = request.POST.get('category_type')
        
        image_gallery_data = []
        image_url = []
        image_gallery = []     
        image_binary_data = []   
        category_list = Category.objects.all().values()
        if category_type != '0' and description == '' and title == '':
            image_gallery = ImageGallery.objects.filter(Q(category_type = category_type)).values()
        elif category_type == '0' and description != '' and title == '':           
            image_gallery = ImageGallery.objects.filter(Q(description__contains = description)).values()
        elif category_type == '0' and description == '' and title != '':           
            image_gallery = ImageGallery.objects.filter(Q(title__contains = title)).values()
        elif category_type != '0' and description != '' and title == '':           
            image_gallery = ImageGallery.objects.filter(Q(category_type = category_type) & 
                                                        Q(description__contains = description)).values()
        elif category_type != '0' and description == '' and title != '':           
            image_gallery = ImageGallery.objects.filter(Q(category_type = category_type) & 
                                                        Q(title__contains = title)).values()
        elif category_type == '0' and description != '' and title != '':           
            image_gallery = ImageGallery.objects.filter(Q(description__contains = description) & 
                                                        Q(title__contains = title)).values()
        else:
            image_gallery = ImageGallery.objects.filter(Q(category_type = category_type) & Q(description__contains = description) & 
                                                        Q(title__contains = title)).values()

        for image in image_gallery:
            url = reverse('image_summary', kwargs={'id': image["id"]})            
            image_url.append(url)
            img_bytes_data = base64.b64encode(image["image_data"]).decode('utf-8')
            image_binary_data.append(img_bytes_data)
            result = {
                'id': image["id"],
                'title': image["title"],
                'description': image["description"],
                'category_type': image["category_type_id"],
            }
            image_gallery_data.append(result)
  
        return JsonResponse({"query_data": list(image_gallery_data), "category": list(category_list), "image_url" : list(image_url), "image_bytes_data" : list(image_binary_data), "responseCode": 200}, status=200, safe=False)
     except Exception as ex:
         return JsonResponse({"message": ex, "responseCode": 400}, status=200)

     

        

    

      