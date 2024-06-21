from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # Your other paths here

    # Path for login
     path('login/', views.login_user, name='login'),

    # Path for dealer reviews view
      path('dealer/<int:dealer_id>/reviews/', views.get_dealer_reviews, name='dealer_reviews'),

    # Path for add a review view
      path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),

    # Path for get_cars view
    path('get_cars/', views.get_cars, name='getcars'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
