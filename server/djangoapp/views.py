from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from datetime import datetime
from .populate import initiate  # Import initiate function
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

def logout_request(request):
    logout(request)
    return JsonResponse({"status": "Logged out"})

@csrf_exempt
def registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        email = data.get('email')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, email, password)
            return JsonResponse({"userName": username, "status": "Registered"})
        else:
            return JsonResponse({"error": "Username already exists"}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()  # Ensure data is populated if not present

    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        print(f"CarModel: {car_model.name}, CarMake: {car_model.car_make.name}")  # Print debug info
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})

    print(f"Cars: {cars}")  # Print final cars list

    return JsonResponse({"CarModels": cars})

# Optional: Other views can be added as needed

# Example view for getting dealer details
# def get_dealer_details(request, dealer_id):
#     dealer = get_object_or_404(Dealer, id=dealer_id)
#     return JsonResponse({"DealerName": dealer.name, "Location": dealer.location})
