import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth
from .models import DealerReview


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(f"GET request to: {url}")
    try:
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key))
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
        response = None

    if response:
        status_code = response.status_code
        print(f"Response status: {status_code}")
        try:
            json_data = response.json()
        except json.JSONDecodeError as json_err:
            print(f"JSON decoding error: {json_err}")
            json_data = None
        return json_data

    return None

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        try:
            reviews = json_result["reviews"]
            for review in reviews:
                dealer_review = DealerReview(
                    dealership=review.get("dealership", ""),
                    name=review.get("name", ""),
                    purchase=review.get("purchase", False),
                    review=review.get("review", ""),
                    purchase_date=review.get("purchase_date", ""),
                    car_make=review.get("car_make", ""),
                    car_model=review.get("car_model", ""),
                    car_year=review.get("car_year", 0),
                    sentiment="",
                    id=review.get("id", "")
                )
                results.append(dealer_review)
        except KeyError as key_err:
            print(f"KeyError: {key_err}")
    return results

