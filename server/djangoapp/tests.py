import json
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from .models import CarMake, CarModel

class ApiTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user('sample','sample@example.com','TrainingCar!2026',first_name='Demo')
    def post(self,url,data):
        return self.client.post(url,data=json.dumps(data),content_type='application/json')
    def test_login_logout_and_denied_login(self):
        self.assertEqual(self.post('/djangoapp/login',{'userName':'sample','password':'bad'}).status_code,401)
        r=self.post('/djangoapp/login',{'userName':'sample','password':'TrainingCar!2026'})
        self.assertEqual(r.json()['status'],'Authenticated')
        self.assertIn('_auth_user_id',self.client.session)
        self.assertEqual(self.client.get('/djangoapp/logout').json()['status'],'Logged out')
        self.assertNotIn('_auth_user_id',self.client.session)
    def test_registration_and_duplicate(self):
        payload={'userName':'newuser','firstName':'New','lastName':'User','email':'new@example.com','password':'TrainingNew!2026'}
        self.assertEqual(self.post('/djangoapp/register',payload).status_code,201)
        self.assertEqual(self.post('/djangoapp/register',payload).status_code,409)
        self.assertTrue(User.objects.get(username='newuser').check_password(payload['password']))
    def test_unauthenticated_review_is_rejected(self):
        self.assertEqual(self.post('/djangoapp/add_review',{}).status_code,401)
    @patch('djangoapp.views.get_request')
    @patch('djangoapp.views.post_review')
    def test_review_uses_authenticated_identity(self,post_review,get_request):
        get_request.return_value=[{'id':1}]
        post_review.return_value={'id':99}
        self.client.force_login(self.user)
        data={'name':'Forged','dealership':1,'review':'Great demo','car_year':2023}
        self.assertEqual(self.post('/djangoapp/add_review',data).status_code,200)
        self.assertEqual(post_review.call_args.args[0]['name'],'Demo')
    @patch('djangoapp.views.get_request',return_value=[])
    def test_filter_and_missing_dealer(self,get_request):
        self.assertEqual(self.client.get('/djangoapp/get_dealers/Kansas').json()['dealers'],[])
        get_request.assert_called_with('fetchDealers/Kansas')
        self.assertEqual(self.client.get('/djangoapp/dealer/999').status_code,404)
    def test_car_model_response(self):
        make=CarMake.objects.create(name='Tesla')
        CarModel.objects.create(car_make=make,name='Model 3',type='SEDAN',year=2023)
        row=self.client.get('/djangoapp/get_cars').json()['CarModels'][0]
        self.assertEqual(row['CarModel'],'Model 3')
