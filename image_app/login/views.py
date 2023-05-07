from django.shortcuts import render
from .models import User
from django.http import JsonResponse
from django.db.models import Q


# Create your views here.
def login_view(request):
    return render(request,'login/login.html')


def register_view(request):
    return render(request,'login/register.html')


def user_registration(request):
    if request.method == 'POST':
        try:
            firstname = request.POST.get('first_name')
            lastname = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('pwd')
            phone_no = request.POST.get('phone_no')
            gender = request.POST.get('gender')

            if User.objects.filter(email_id = email).exists():
                return JsonResponse({"message": 'Email already exists', "responseCode": 220}, status=200)
            new_user = User(firstname = firstname, lastname = lastname, email_id = email,
                            password = password, mobile_no = phone_no, gender = gender)
            new_user.save()
            success = 'Profile created successfully!'
            return JsonResponse({"message": success, "responseCode": 200}, status=200)
        except Exception as ex:
            return JsonResponse({"message": 'Error while processing', "responseCode": 400}, status=200)
    


def authenticate_user(request):
     if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('pwd')
            check_if_user_exists = User.objects.filter(Q(email_id=email) and Q(password=password)).exists()
            
            if check_if_user_exists:
                request.session["user_id"] = User.objects.get(email_id=email).id
                return JsonResponse({"message": "Login successful", "responseCode": 200}, status=200)
            else:
                return JsonResponse({"message": "Invalid username or password", "responseCode": 205}, status=200)            
        except Exception as ex:
            return JsonResponse({"message": 'Error while processing', "responseCode": 400}, status=200)
    