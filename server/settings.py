from enum import Enum
from typing import Dict, List, Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!


class DromSettings:
    BASE_URL = "https://www.drom.ru/catalog/~search/"
    DEFAULT_PARAMS = "wheel=0"
    USER_AGENT ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

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

class SearchParams:
    def __init__(
        self,
        marka: Optional[str] = None,
        model: Optional[str] = None,
        price_min: Optional[int] = None,
        price_max: Optional[int] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        fuel_types: Optional[List[FuelType]] = None,
        drive_types: Optional[List[DriveType]] = None,
        trans_types: Optional[List[TransmissionType]] = None,
        volume_min: Optional[float] = None,
        volume_max: Optional[float] = None,
        power_min: Optional[int] = None,
        power_max: Optional[int] = None,
        page: Optional[int] = None
    ):
        self.marka = marka
        self.model = model
        self.price_min = price_min
        self.price_max = price_max
        self.year_min = year_min
        self.year_max = year_max
        self.fuel_types = fuel_types or []
        self.drive_types = drive_types or []
        self.trans_types = trans_types or []
        self.volume_min = volume_min
        self.volume_max = volume_max
        self.power_min = power_min
        self.power_max = power_max
        self.page = page

    def to_url_params(self) -> str:
        params = []
        
        if self.marka:
            params.append(f"marka={self.marka}")
        if self.model:
            params.append(f"model={self.model}")
        if self.price_min is not None:
            params.append(f"p_start={self.price_min}")
        if self.price_max is not None:
            params.append(f"p_end={self.price_max}")
        if self.year_min is not None:
            params.append(f"y_start={self.year_min}")
        if self.year_max is not None:
            params.append(f"y_end={self.year_max}")
        if self.fuel_types:
            params.extend([f"fuel_type_short%5B%5D={ft.value}" for ft in self.fuel_types])
        if self.drive_types:
            params.extend([f"drive_type_short%5B%5D={dt.value}" for dt in self.drive_types])
        if self.trans_types:
            params.extend([f"trans_type_short%5B%5D={tt.value}" for tt in self.trans_types])
        if self.volume_min is not None:
            params.append(f"volume_from={self.volume_min}")
        if self.volume_max is not None:
            params.append(f"volume_to={self.volume_max}")
        if self.power_min is not None:
            params.append(f"power_from={self.power_min}")
        if self.power_max is not None:
            params.append(f"power_to={self.power_max}")
        if self.page is not None:
            params.append(f"page={self.page}")

        return "&".join(params) 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'server.middleware.IPRestrictionMiddleware',
]

# IP Restriction Settings
ALLOWED_IPS = [
    '127.0.0.1',  # localhost
    '::1',        # IPv6 localhost
    # Add your allowed IP addresses here
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'drom'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Email settings
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True' 