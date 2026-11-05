from django.core.management.base import BaseCommand
from djangoapp.models import CarMake, CarModel
class Command(BaseCommand):
    help = 'Create idempotent educational vehicle examples'
    def handle(self,*args,**options):
        for brand,model,kind in [('Toyota','Camry','SEDAN'),('Toyota','RAV4','SUV'),('Honda','Civic','SEDAN'),('Ford','Escape','SUV'),('Tesla','Model 3','SEDAN')]:
            make,_=CarMake.objects.get_or_create(name=brand,defaults={'description':brand+' sample vehicles'})
            CarModel.objects.get_or_create(car_make=make,name=model,year=2023,defaults={'type':kind})
        self.stdout.write(self.style.SUCCESS('Vehicle examples ready'))
