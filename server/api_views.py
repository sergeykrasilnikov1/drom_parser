from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from .api import DromAPI, DromAPIError
from .settings import SearchParams, FuelType, DriveType, TransmissionType
from .serializers import SearchParamsSerializer

class SearchAPIView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            serializer = SearchParamsSerializer(data=request.data)
            if not serializer.is_valid():
                if 'error' in serializer.errors and 'details' in serializer.errors:
                    return Response(
                        {
                            'error': serializer.errors['error'],
                            'details': serializer.errors['details']
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {
                        'error': 'Validation error',
                        'details': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            fuel_types = []
            if 'fuel_types' in serializer.validated_data:
                try:
                    fuel_types = [FuelType(ft) for ft in serializer.validated_data['fuel_types']]
                except ValueError as e:
                    return Response(
                        {
                            'error': 'Invalid fuel type value',
                            'details': str(e)
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            drive_types = []
            if 'drive_types' in serializer.validated_data:
                try:
                    drive_types = [DriveType(dt) for dt in serializer.validated_data['drive_types']]
                except ValueError as e:
                    return Response(
                        {
                            'error': 'Invalid drive type value',
                            'details': str(e)
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            trans_types = []
            if 'trans_types' in serializer.validated_data:
                try:
                    trans_types = [TransmissionType(tt) for tt in serializer.validated_data['trans_types']]
                except ValueError as e:
                    return Response(
                        {
                            'error': 'Invalid transmission type value',
                            'details': str(e)
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Create search parameters
            search_params = SearchParams(
                marka=serializer.validated_data.get('marka'),
                model=serializer.validated_data.get('model'),
                price_min=serializer.validated_data.get('price_min'),
                price_max=serializer.validated_data.get('price_max'),
                year_min=serializer.validated_data.get('year_min'),
                year_max=serializer.validated_data.get('year_max'),
                fuel_types=fuel_types,
                drive_types=drive_types,
                trans_types=trans_types,
                volume_min=serializer.validated_data.get('volume_min'),
                volume_max=serializer.validated_data.get('volume_max'),
                power_min=serializer.validated_data.get('power_min'),
                power_max=serializer.validated_data.get('power_max'),
            )

            # Perform search
            api = DromAPI()
            results = api.search(search_params)

            return Response(results, status=status.HTTP_200_OK)

        except DromAPIError as e:
            return Response(
                {
                    'error': 'API Error',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {
                    'error': 'Unexpected error',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )