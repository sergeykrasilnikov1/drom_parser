import requests
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class FuelType(Enum):
    PETROL = "0"
    GAS = "1"
    DIESEL = "2"

class DriveType(Enum):
    FRONT = "1"
    REAR = "2"

class TransmissionType(Enum):
    MANUAL = "1"
    AUTOMATIC = "3"

@dataclass
class SearchParams:
    marka: Optional[str] = None
    model: Optional[str] = None
    price_min: Optional[int] = None
    price_max: Optional[int] = None
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    fuel_types: Optional[List[FuelType]] = None
    drive_types: Optional[List[DriveType]] = None
    trans_types: Optional[List[TransmissionType]] = None
    volume_min: Optional[float] = None
    volume_max: Optional[float] = None
    power_min: Optional[int] = None
    power_max: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {}
        if self.marka:
            data['marka'] = self.marka
        if self.model:
            data['model'] = self.model
        if self.price_min is not None:
            data['price_min'] = self.price_min
        if self.price_max is not None:
            data['price_max'] = self.price_max
        if self.year_min is not None:
            data['year_min'] = self.year_min
        if self.year_max is not None:
            data['year_max'] = self.year_max
        if self.fuel_types:
            data['fuel_types'] = [ft.value for ft in self.fuel_types]
        if self.drive_types:
            data['drive_types'] = [dt.value for dt in self.drive_types]
        if self.trans_types:
            data['trans_types'] = [tt.value for tt in self.trans_types]
        if self.volume_min is not None:
            data['volume_min'] = self.volume_min
        if self.volume_max is not None:
            data['volume_max'] = self.volume_max
        if self.power_min is not None:
            data['power_min'] = self.power_min
        if self.power_max is not None:
            data['power_max'] = self.power_max
        return data

class DromAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api/search/"

    def search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.get(
                self.api_url,
                json=params,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                try:
                    return e.response.json()
                except json.JSONDecodeError:
                    return {
                        'error': 'Invalid parameters',
                        'details': {
                            'message': str(e)
                        }
                    }
            return {
                'error': 'HTTP Error',
                'details': {
                    'message': str(e)
                }
            }
        except requests.exceptions.RequestException as e:
            return {
                'error': 'Request Error',
                'details': {
                    'message': str(e)
                }
            }

    def test_basic_search(self):
        """Test basic search with minimal parameters"""
        params = SearchParams(
        )
        print("\nTesting basic search:")
        print(f"Parameters: {params.to_dict()}")
        result = self.search(params.to_dict())
        print(f"Results: {json.dumps(result, indent=2, ensure_ascii=False)}")

    def test_invalid_parameter(self):
        """Test search with invalid parameter name"""
        params = {
            'price_min': 55000000,  # Invalid parameter name
        }
        print("\nTesting invalid parameter name:")
        print(f"Parameters: {params}")
        result = self.search(params)
        print(f"Results: {json.dumps(result, indent=2, ensure_ascii=False)}")

    def test_invalid_enum_value(self):
        """Test search with invalid enum value"""
        params = {
            'marka': 'Toyota',
            'fuel_types': ['invalid']  # Invalid fuel type
        }
        print("\nTesting invalid enum value:")
        print(f"Parameters: {params}")
        result = self.search(params)
        print(f"Results: {json.dumps(result, indent=2, ensure_ascii=False)}")

    def test_invalid_data_type(self):
        """Test search with invalid data type"""
        params = {
            'marka': 'Toyota',
            'price_min': 'not_a_number'  # Invalid data type
        }
        print("\nTesting invalid data type:")
        print(f"Parameters: {params}")
        result = self.search(params)
        print(f"Results: {json.dumps(result, indent=2, ensure_ascii=False)}")

    def run_all_tests(self):
        """Run all test scenarios"""
        print("Starting API tests...")
        # self.test_basic_search()
        self.test_invalid_parameter()
        # self.test_invalid_enum_value()
        # self.test_invalid_data_type()
        print("\nAll tests completed!")

if __name__ == "__main__":
    # Create tester instance
    tester = DromAPITester()
    
    # Run all tests
    for i in range(200):
        tester.run_all_tests()
    
    # Or run individual tests
    # tester.test_basic_search()
    # tester.test_invalid_parameter()
    # tester.test_invalid_enum_value()
    # tester.test_invalid_data_type() 