import os
import django
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drom.settings')
django.setup()

from server.models import Car, Complectation
from server.api import DromAPI
from server.settings import SearchParams

def parse_and_save_cars():
    api = DromAPI()

    search_params = SearchParams(
        price_min=0
    )
    
    try:
        results = api.search(search_params)
        
        for car_data in results:
            car, created = Car.objects.update_or_create(
                model=car_data['model'],
                defaults={
                    'model_url': car_data['model_url'],
                    'image_url': car_data['image_url']
                }
            )

            for complectation_data in car_data['complectation']:
                Complectation.objects.update_or_create(
                    car=car,
                    name=complectation_data['name'],
                    defaults={
                        'volume': complectation_data['features']['volume'],
                        'fuel_type': complectation_data['features']['fuel_type'],
                        'power': complectation_data['features']['power'],
                        'transmission': complectation_data['features']['transmission'],
                        'drive': complectation_data['features']['drive'],
                        'price': complectation_data['price'],
                        'year': complectation_data['year']
                    }
                )
            
            print(f"Processed car: {car.model}")
            # time.sleep(1)
        
        print("Parsing completed successfully!")
        
    except Exception as e:
        print(f"Error during parsing: {str(e)}")

if __name__ == "__main__":
    parse_and_save_cars() 