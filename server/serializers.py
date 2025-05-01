from rest_framework import serializers
from .settings import FuelType, DriveType, TransmissionType

class SearchParamsSerializer(serializers.Serializer):
    marka = serializers.CharField(required=False, allow_null=True)
    model = serializers.CharField(required=False, allow_null=True)
    price_min = serializers.IntegerField(required=False, allow_null=True)
    price_max = serializers.IntegerField(required=False, allow_null=True)
    year_min = serializers.IntegerField(required=False, allow_null=True)
    year_max = serializers.IntegerField(required=False, allow_null=True)
    fuel_types = serializers.MultipleChoiceField(
        choices=[(ft.value, ft.name) for ft in FuelType],
        required=False,
        allow_null=True
    )
    drive_types = serializers.MultipleChoiceField(
        choices=[(dt.value, dt.name) for dt in DriveType],
        required=False,
        allow_null=True
    )
    trans_types = serializers.MultipleChoiceField(
        choices=[(tt.value, tt.name) for tt in TransmissionType],
        required=False,
        allow_null=True
    )
    volume_min = serializers.FloatField(required=False, allow_null=True)
    volume_max = serializers.FloatField(required=False, allow_null=True)
    power_min = serializers.IntegerField(required=False, allow_null=True)
    power_max = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, data):
        # List of valid parameter names
        valid_params = {
            'marka', 'model', 'price_min', 'price_max', 'year_min', 'year_max',
            'fuel_types', 'drive_types', 'trans_types', 'volume_min', 'volume_max',
            'power_min', 'power_max'
        }

        invalid_params = set(self.initial_data.keys()) - valid_params
        if invalid_params:
            raise serializers.ValidationError({
                'error': 'Invalid parameters',
                'details': {
                    'invalid_params': list(invalid_params),
                    'valid_params': list(valid_params),
                    'message': f"Invalid parameter(s): {', '.join(invalid_params)}. Please use only valid parameters."
                }
            })

        return data 