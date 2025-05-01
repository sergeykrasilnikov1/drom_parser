# Drom Car Search API

## Overview
This API provides access to car search functionality on drom.ru. It allows searching for cars based on various parameters and returns detailed information about matching vehicles. The API automatically fetches all available pages of results.

## Base URL
```
http://your-domain.com/api/search/
```

## Endpoints

### Search Cars
```
GET /api/search/
```

#### Request Parameters
```json
{
    "marka": "string",           // Car brand (optional)
    "model": "string",           // Car model (optional)
    "price_min": number,         // Minimum price (optional)
    "price_max": number,         // Maximum price (optional)
    "year_min": number,          // Minimum year (optional)
    "year_max": number,          // Maximum year (optional)
    "fuel_types": [              // Fuel types (optional)
        "0",                     // Petrol
        "1",                     // Diesel
        "2",                     // Electricity
        "3",                     // Gas
        "4"                      // Gas/Diesel
    ],
    "drive_types": [             // Drive types (optional)
        "1",                     // Front
        "2",                     // Back
        "3"                      // Full
    ],
    "trans_types": [             // Transmission types (optional)
        "0",                     // MT
        "1",                     // CVT
        "2",                     // AT
        "3",                     // Robot
        "4"                      // Reducer
    ],
    "volume_min": number,        // Minimum engine volume (optional)
    "volume_max": number,        // Maximum engine volume (optional)
    "power_min": number,         // Minimum power (optional)
    "power_max": number          // Maximum power (optional)
}
```

#### Response Format
```json
[
    {
        "model": "string",           // Car model name
        "model_url": "string",       // URL to the car listing
        "image_url": "string",       // URL to the car image
        "complectation": [           // List of complectations
            {
                "name": "string",    // Complectation name
                "features": {         // Car features
                    "volume": "string",      // Engine volume (e.g., "2.5 л")
                    "fuel_type": "string",   // Fuel type (e.g., "бензин")
                    "power": "string",       // Power (e.g., "181 л.с.")
                    "transmission": "string", // Transmission type (e.g., "АКПП")
                    "drive": "string"        // Drive type (e.g., "передний привод")
                },
                "price": "string",   // Car price
                "year": "string"     // Car year
            }
        ]
    }
]
```

#### Example Response
```json
[
    {
        "model": "Toyota Camry",
        "model_url": "https://www.drom.ru/catalog/toyota/camry/...",
        "image_url": "https://example.com/image.jpg",
        "complectation": [
            {
                "name": "Comfort",
                "features": {
                    "volume": "2.5 л",
                    "fuel_type": "бензин",
                    "power": "181 л.с.",
                    "transmission": "АКПП",
                    "drive": "передний привод"
                },
                "price": "1 500 000 ₽",
                "year": "2022"
            },
            {
                "name": "Prestige",
                "features": {
                    "volume": "3.5 л",
                    "fuel_type": "бензин",
                    "power": "249 л.с.",
                    "transmission": "АКПП",
                    "drive": "полный привод"
                },
                "price": "2 000 000 ₽",
                "year": "2023"
            }
        ]
    }
]
```

#### Error Responses

##### 400 Bad Request
```json
{
    "error": "string",  // Description of the validation error
    "details": {
        "message": "string"  // Detailed error message
    }
}
```

##### 500 Internal Server Error
```json
{
    "error": "string",  // Description of the server error
    "details": {
        "message": "string"  // Detailed error message
    }
}
```

## Rate Limiting
Currently, there are no rate limits implemented.

## Error Handling
The API uses standard HTTP status codes to indicate the success or failure of a request:
- 200: Success
- 400: Bad Request (invalid parameters)
- 500: Internal Server Error

## Notes
- All price values should be in rubles
- Year values should be in YYYY format
- Engine volume should be in liters
- Power should be in horsepower
- The API automatically fetches all available pages of results 

### Search Cars from Database
```
GET /api/search_cars/
```

This endpoint searches for cars in the local database based on various parameters. It returns cars that have at least one complectation matching the specified criteria.

#### Request Parameters
All parameters are optional. If no parameters are provided, all cars with their complectations will be returned.

```json
{
    "model": "string",           // Car model name (partial match, case-insensitive)
    "year_min": "string",        // Minimum year (e.g., "2020")
    "year_max": "string",        // Maximum year (e.g., "2023")
    "price_min": "string",       // Minimum price (e.g., "1000000")
    "price_max": "string",       // Maximum price (e.g., "5000000")
    "fuel_type": "string",       // Fuel type (e.g., "бензин", "дизель")
    "drive_type": "string",      // Drive type (e.g., "передний", "задний")
    "transmission": "string",    // Transmission type (e.g., "автомат", "механика")
    "volume_min": "string",      // Minimum engine volume (e.g., "1.6")
    "volume_max": "string",      // Maximum engine volume (e.g., "3.0")
    "power_min": "string",       // Minimum power (e.g., "100")
    "power_max": "string"        // Maximum power (e.g., "300")
}
```

#### Response Format
```json
{
    "status": "success",
    "count": number,             // Number of cars found
    "results": [                 // List of cars
        {
            "id": number,        // Car ID
            "model": "string",   // Car model name
            "model_url": "string", // URL to the car model page
            "image_url": "string", // URL to the car image
            "complectations": [  // List of matching complectations
                {
                    "id": number,           // Complectation ID
                    "name": "string",       // Complectation name
                    "volume": "string",     // Engine volume
                    "fuel_type": "string",  // Fuel type
                    "power": "string",      // Power
                    "transmission": "string", // Transmission type
                    "drive": "string",      // Drive type
                    "price": "string",      // Price
                    "year": "string"        // Year
                }
            ]
        }
    ]
}
```

#### Example Request
```
GET /api/search_cars/?model=Toyota&year_min=2020&price_max=5000000
```

#### Example Response
```json
{
    "status": "success",
    "count": 2,
    "results": [
        {
            "id": 1,
            "model": "Toyota Camry",
            "model_url": "https://example.com/toyota-camry",
            "image_url": "https://example.com/toyota-camry.jpg",
            "complectations": [
                {
                    "id": 1,
                    "name": "Comfort",
                    "volume": "2.5 л",
                    "fuel_type": "бензин",
                    "power": "181 л.с.",
                    "transmission": "автомат",
                    "drive": "передний",
                    "price": "2500000",
                    "year": "2021"
                }
            ]
        }
    ]
}
```

#### Notes
- All text-based searches are case-insensitive and support partial matches
- A car is included in the results only if it has at least one complectation matching all specified criteria
- If multiple complectations match the criteria, all of them will be included in the response
- The endpoint returns data from the local database, which may be different from the live Drom.ru data 