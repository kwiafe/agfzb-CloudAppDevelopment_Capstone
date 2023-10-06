from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf



# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
  
        else:
            # Handle invalid login
            pass  # You can add your own logic here

    return render(request, 'login.html')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return render(request, 'djangoapp/index.html')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        # Create a new user
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)

        # Log in the user (optional)
        # You can remove the next two lines if you don't want to automatically log in the user after signup
        from django.contrib.auth import login
        login(request, user)

        return render(request, 'djangoapp/index.html')

    return render(request, 'djangoapp/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://6655881d-fa8a-4edb-8f45-6c19cf0732f5-bluemix.cloudantnosqldb.appdomain.cloud"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context['dealerships'] = dealerships
        # Return a list of dealer short name
    return render(request, 'djangoapp/index.html', context)
# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...


def get_dealer_details(request, dealer_id):
    url = "URL_TO_YOUR_REVIEWS_GET_CLOUD_FUNCTION"  # Replace with the actual URL
    reviews = get_dealer_reviews_from_cf(url, dealer_id)
    context = {
        'reviews': reviews
    }
    return render(request, 'dealer_details.html', context)


def add_review(request, dealer_id):
    context = {}

    if request.method == 'GET':
        # Step 1: Query the cars with the dealer id to be reviewed
        # (Assuming you have a function to get cars by dealer id)
        cars = get_cars_by_dealer_id(dealer_id)

        # Append the queried cars into context
        context['cars'] = cars

        # Render add_review.html
        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == 'POST':
        # Step 2: Update json_payload with actual values from the review form
        json_payload = {
            "reviewer_id": request.user.id,  # Assuming you have user authentication
            "dealership": dealer_id,
            "review": request.POST.get('content'),  # Assuming the form input is named 'content'
            "purchase": request.POST.get('purchasecheck'),  # Assuming the form input is a checkbox named 'purchasecheck'
            "purchase_date": datetime.utcnow().isoformat(),  # Current datetime in ISO format
            "car_make": request.POST.get('car_make'),  # Assuming the form input is named 'car_make'
            "car_model": request.POST.get('car_model'),  # Assuming the form input is named 'car_model'
            "car_year": datetime.strptime(request.POST.get('purchasedate'), "%Y-%m-%d").strftime("%Y")  # Assuming date format is 'YYYY-MM-DD'
        }

        # Step 3: Make a POST request to submit the review
        response = requests.post("URL_TO_YOUR_REVIEWS_POST_CLOUD_FUNCTION", json=json_payload)

        if response.status_code == 200:
            # Step 4: Redirect user to the dealer details page after review submission
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
