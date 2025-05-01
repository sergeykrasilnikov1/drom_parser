from django.shortcuts import render
from django.views import View
from django.core.exceptions import ValidationError
from .api import DromAPI, DromAPIError
from .settings import SearchParams, FuelType, DriveType, TransmissionType
from django.http import JsonResponse
from django.db.models import Q
from .models import Car, Complectation
from django.views.generic import TemplateView

class SearchView(TemplateView):
    template_name = 'search.html'

    def get(self, request):
        return render(request, 'search.html')

    def post(self, request):
        try:
            # Parse form data
            fuel_types = []
            if 'fuel_type' in request.POST:
                for value in request.POST.getlist('fuel_type'):
                    try:
                        fuel_types.append(FuelType(value))
                    except ValueError:
                        raise ValidationError(f"Invalid fuel type: {value}")

            drive_types = []
            if 'drive_type' in request.POST:
                for value in request.POST.getlist('drive_type'):
                    try:
                        drive_types.append(DriveType(value))
                    except ValueError:
                        raise ValidationError(f"Invalid drive type: {value}")

            trans_types = []
            if 'trans_type' in request.POST:
                for value in request.POST.getlist('trans_type'):
                    try:
                        trans_types.append(TransmissionType(value))
                    except ValueError:
                        raise ValidationError(f"Invalid transmission type: {value}")

            # Create search parameters
            search_params = SearchParams(
                marka=request.POST.get('marka'),
                model=request.POST.get('model'),
                price_min=request.POST.get('price_min'),
                price_max=request.POST.get('price_max'),
                year_min=request.POST.get('year_min'),
                year_max=request.POST.get('year_max'),
                fuel_types=fuel_types,
                drive_types=drive_types,
                trans_types=trans_types,
                volume_min=request.POST.get('volume_min'),
                volume_max=request.POST.get('volume_max'),
                power_min=request.POST.get('power_min'),
                power_max=request.POST.get('power_max'),
            )

            # Perform search
            api = DromAPI()
            results = api.search(search_params)

            return render(request, 'search.html', {'results': results})

        except ValidationError as e:
            return render(request, 'search.html', {'error': str(e)})
        except DromAPIError as e:
            return render(request, 'search.html', {'error': f"API Error: {str(e)}"})
        except Exception as e:
            return render(request, 'search.html', {'error': f"Unexpected error: {str(e)}"})

def search_cars(request):
    query = Q()
    
    # Получаем параметры из запроса
    model = request.GET.get('model')
    year_min = request.GET.get('year_min')
    year_max = request.GET.get('year_max')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    fuel_type = request.GET.get('fuel_type')
    drive_type = request.GET.get('drive_type')
    transmission = request.GET.get('transmission')
    volume_min = request.GET.get('volume_min')
    volume_max = request.GET.get('volume_max')
    power_min = request.GET.get('power_min')
    power_max = request.GET.get('power_max')

    # Строим запрос
    if model:
        query &= Q(model__icontains=model)
    
    # Получаем автомобили
    cars = Car.objects.filter(query).prefetch_related('complectations')
    
    # Фильтруем комплектации
    complectations_query = Q()
    if year_min:
        complectations_query &= Q(year__gte=year_min)
    if year_max:
        complectations_query &= Q(year__lte=year_max)
    if price_min:
        complectations_query &= Q(price__gte=price_min)
    if price_max:
        complectations_query &= Q(price__lte=price_max)
    if fuel_type:
        complectations_query &= Q(fuel_type__icontains=fuel_type)
    if drive_type:
        complectations_query &= Q(drive__icontains=drive_type)
    if transmission:
        complectations_query &= Q(transmission__icontains=transmission)
    if volume_min:
        complectations_query &= Q(volume__gte=volume_min)
    if volume_max:
        complectations_query &= Q(volume__lte=volume_max)
    if power_min:
        complectations_query &= Q(power__gte=power_min)
    if power_max:
        complectations_query &= Q(power__lte=power_max)

    # Формируем ответ
    results = []
    for car in cars:
        complectations = car.complectations.filter(complectations_query)
        if complectations.exists():
            car_data = {
                'id': car.id,
                'model': car.model,
                'model_url': car.model_url,
                'image_url': car.image_url,
                'complectations': []
            }
            
            for comp in complectations:
                car_data['complectations'].append({
                    'id': comp.id,
                    'name': comp.name,
                    'volume': comp.volume,
                    'fuel_type': comp.fuel_type,
                    'power': comp.power,
                    'transmission': comp.transmission,
                    'drive': comp.drive,
                    'price': comp.price,
                    'year': comp.year
                })
            
            results.append(car_data)

    return JsonResponse({
        'status': 'success',
        'count': len(results),
        'results': results
    })
