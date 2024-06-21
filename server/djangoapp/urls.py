from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # Paths for dealer operations
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
    path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),

    # Path for getting cars
    path('get_cars/', views.get_cars, name='get_cars'),

    # Optional: Add other paths as needed

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
