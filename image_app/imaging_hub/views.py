from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, Http404
from .models import Category, ImageGallery
from login.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q


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
            title = request.POST.get('title')
            description = request.POST.get('description')
            category_type = request.POST.get('category_type')
            category_model = Category.objects.get(pk = int(category_type))
            transaction_date = timezone.now()
            image_gallery = ImageGallery(image  = image_file, title = title, description = description, 
                                    category_type = category_model, created_by = request.session['user_id'],
                                    created_date = transaction_date)
            image_gallery.save()
            return JsonResponse({"message": "Image upload successful", "responseCode": 200}, status=200)
        except Exception as ex:
            return JsonResponse({"message": "Error while procesing", "responseCode": 400}, status=200)
     

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
                "image_url": image_gallery.image,
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
        
        image_url = []
        image_gallery = []        
        category_list = Category.objects.all().values()
        if category_type != '' and description == '' and title == '':
            image_gallery = ImageGallery.objects.filter(Q(category_type = category_type)).values()
        elif category_type == '' and description != '' and title == '':           
            image_gallery = ImageGallery.objects.filter(Q(description__contains = description)).values()
        elif category_type == '' and description == '' and title != '':           
            image_gallery = ImageGallery.objects.filter(Q(title__contains = title)).values()
        elif category_type != '' and description != '' and title == '':           
            image_gallery = ImageGallery.objects.filter(Q(category_type = category_type) & 
                                                        Q(description__contains = description)).values()
        elif category_type != '' and description == '' and title != '':           
            image_gallery = ImageGallery.objects.filter(Q(category_type = category_type) & 
                                                        Q(title__contains = title)).values()
        elif category_type == '' and description != '' and title != '':           
            image_gallery = ImageGallery.objects.filter(Q(description__contains = description) & 
                                                        Q(title__contains = title)).values()
        else:
            image_gallery = ImageGallery.objects.filter(Q(category_type = category_type) & Q(description__contains = description) & 
                                                        Q(title__contains = title)).values()

        for image in image_gallery:
            url = reverse('image_summary', kwargs={'id': image["id"]})            
            image_url.append(url)
  
        return JsonResponse({"query_data": list(image_gallery), "category": list(category_list), "image_url" : list(image_url), "responseCode": 200}, status=200, safe=False)
     except Exception as ex:
         return JsonResponse({"message": ex, "responseCode": 400}, status=200)

     

        

    

      