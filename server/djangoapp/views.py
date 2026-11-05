import json
from functools import wraps
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .models import CarModel
from .restapis import get_request, post_review, analyze_review_sentiments

def api_errors(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except (ValueError, KeyError, TypeError, ValidationError) as exc:
            return JsonResponse({'status':400,'error':str(exc)},status=400)
        except requests.RequestException:
            return JsonResponse({'status':503,'error':'A backend service is unavailable.'},status=503)
    return wrapped

@csrf_exempt
@require_POST
@api_errors
def login_user(request):
    data = json.loads(request.body)
    user = authenticate(request,username=data['userName'],password=data['password'])
    if user is None:
        return JsonResponse({'status':'Invalid credentials'},status=401)
    login(request,user)
    return JsonResponse({'status':'Authenticated','userName':user.username,'firstName':user.first_name,'lastName':user.last_name})

@require_GET
def logout_request(request):
    logout(request)
    return JsonResponse({'status':'Logged out', 'userName': ''})

@csrf_exempt
@require_POST
@api_errors
def registration(request):
    data = json.loads(request.body)
    username = data['userName'].strip()
    if not username or not data['email'].strip():
        raise ValueError('Username and email are required.')
    user = User(username=username,first_name=data['firstName'],last_name=data['lastName'],email=data['email'])
    validate_password(data['password'],user)
    user.set_password(data['password'])
    try:
        with transaction.atomic():
            user.save()
    except IntegrityError:
        return JsonResponse({'status':409,'error':'Username already exists.'},status=409)
    login(request,user)
    return JsonResponse({'status':'Authenticated','userName':username,'firstName':user.first_name,'lastName':user.last_name},status=201)

@require_GET
@api_errors
def get_dealerships(request,state='All'):
    endpoint = 'fetchDealers' if state == 'All' else f'fetchDealers/{state}'
    return JsonResponse({'status':200,'dealers':get_request(endpoint)})

@require_GET
@api_errors
def get_dealer_details(request,dealer_id):
    dealers = get_request(f'fetchDealer/{dealer_id}')
    return JsonResponse({'status':200 if dealers else 404,'dealer':dealers},status=200 if dealers else 404)

@require_GET
@api_errors
def get_dealer_reviews(request,dealer_id):
    reviews = get_request(f'fetchReviews/dealer/{dealer_id}')
    for review in reviews:
        review.update(analyze_review_sentiments(review['review']))
    return JsonResponse({'status':200,'reviews':reviews})

@require_GET
def get_cars(request):
    cars = [{'id':c.id,'CarMake':c.car_make.name,'CarModel':c.name,'CarYear':c.year} for c in CarModel.objects.select_related('car_make').order_by('car_make__name','name')]
    return JsonResponse({'status':200,'CarModels':cars})

@csrf_exempt
@require_POST
@api_errors
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status':401,'error':'Please log in.'},status=401)
    data = json.loads(request.body)
    if not data['review'].strip():
        raise ValueError('Review is required.')
    dealer_id = int(data['dealership'])
    if not get_request(f'fetchDealer/{dealer_id}'):
        raise ValueError('Unknown dealership.')
    data['name'] = request.user.get_full_name() or request.user.username
    data['dealership'] = dealer_id
    data['car_year'] = int(data['car_year'])
    return JsonResponse({'status':200,'review':post_review(data)})

