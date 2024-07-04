import json
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review
import logging

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
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})

    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


@csrf_exempt
@login_required
def add_review(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            response = post_review(data)
            print(response)  # Print the response for debugging
            return JsonResponse({"status": 200, "message": "Review added successfully"})
        except Exception as e:
            print(str(e))  # Print the exception for debugging
            return JsonResponse({"status": 500, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 405, "message": "Method not allowed"})
