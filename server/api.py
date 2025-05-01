import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from .settings import DromSettings, SearchParams, FuelType, DriveType, TransmissionType
from django.core.exceptions import ValidationError

class DromAPIError(Exception):
    """Base exception for Drom API errors"""
    pass

class DromAPI:
    def __init__(self):
        self.base_url = DromSettings.BASE_URL
        self.default_params = DromSettings.DEFAULT_PARAMS
        self.headers = {"User-Agent": DromSettings.USER_AGENT}

    def _build_url(self, search_params: SearchParams) -> str:
        params = search_params.to_url_params()
        url = f"{self.base_url}?{self.default_params}"
        if params:
            url += f"&{params}"
        if hasattr(search_params, 'page') and search_params.page is not None:
            url += f"&page={search_params.page}"
        return url

    def _parse_response(self, html_content: str) -> List[Dict]:
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            items = soup.find_all("tr", class_="b-table__row")
            results = []
            current_model = None
            features = None
            i = 0
            while i < len(items):

                try:
                    item = items[i] if i  < len(items) else None
                    if item.find("a", class_="openComplectations"):
                        i+=1
                        continue
                    image_tag = item.find("img", class_="b-image__image")
                    image_url = image_tag["src"] if image_tag else ""

                    model_tag = item.find("a", class_="b-link")
                    has_b_tag = bool(item.find("b"))


                    if model_tag and has_b_tag:
                        model_name = model_tag.text.strip()
                        model_url = f"https://www.drom.ru{model_tag['href']}"
                        raw_features = item.find("b").text.strip() if item.find("b") else ""

                        features_parts = [part.strip() for part in raw_features.split(',')]
                        features = {
                            'volume': features_parts[0] if len(features_parts)>0 else "",
                            'fuel_type': features_parts[1] if len(features_parts)>1 else "",
                            'power': features_parts[2] if len(features_parts)>2 else "",
                            'transmission': features_parts[3] if len(features_parts)>3 else "",
                            'drive': features_parts[4] if len(features_parts)>4 else "",
                        }

                        current_model = {
                            'model': model_name,
                            'model_url': model_url,
                            'image_url': image_url,
                            'complectation': []
                        }
                        results.append(current_model)
                        i+=1
                    else:
                        next_row = items[i] if i  < len(items) else None
                        if next_row:
                            if item.find("b"):
                                raw_features = item.find("b").text.strip()
                                features_parts = raw_features.split(',')
                                features = {
                                    'volume': features_parts[0] if len(features_parts) > 0 else "",
                                    'fuel_type': features_parts[1] if len(features_parts) > 1 else "",
                                    'power': features_parts[2] if len(features_parts) > 2 else "",
                                    'transmission': features_parts[3] if len(features_parts) > 3 else "",
                                    'drive': features_parts[4] if len(features_parts) > 4 else "",
                                }
                                
                                # for part in features_parts:
                                #     if 'л.' in part:
                                #         features['volume'] = part.strip()
                                #     elif any(fuel in part.lower() for fuel in ['бензин', 'дизель', 'газ']):
                                #         features['fuel_type'] = part.strip()
                                #     elif 'л.с.' in part:
                                #         features['power'] = part.strip()
                                #     elif any(trans in part.lower() for trans in ['акпп', 'мкпп', 'автомат', 'механика']):
                                #         features['transmission'] = part.strip()
                                #     elif any(drive in part.lower() for drive in ['передний', 'задний', 'полный']):
                                #         features['drive'] = part.strip()
                                i+=1
                                continue
                            trim_td = next_row.find("td")
                            year_td = trim_td.find_next("td") if trim_td else None
                            price_td = year_td.find_next("td") if year_td else None

                            trim_level = trim_td.text.strip() if trim_td else ""
                            year = year_td.text.strip() if year_td else ""
                            price = price_td.text.strip() if year_td else ""
                            if current_model:
                                current_model['complectation'].append({
                                    'name': trim_level,
                                    'features': features,
                                    'price': price,
                                    'year': year
                                })
                            i += 1  # Move to next row
                            continue

                except Exception as e:
                    raise DromAPIError(f"Error parsing item{len(items)} {i}: {str(e)}")

            return results
        except Exception as e:
            raise DromAPIError(f"Error parsing response: {str(e)}")

    def search(self, search_params: SearchParams) -> List[Dict]:
        try:
            all_results = []
            page = 1
            
            while True:
                # Build URL with current page
                url = f"{self._build_url(search_params)}&page={page}"
                response = requests.get(url, headers=self.headers)
                
                if response.status_code != 200:
                    raise DromAPIError(f"API request failed with status code {response.status_code}")

                page_results = self._parse_response(response.text)

                if not page_results:
                    break
                
                all_results.extend(page_results)

                soup = BeautifulSoup(response.text, "html.parser")
                next_page = soup.find("a", class_="b-pagination__item_next")
                if not next_page or page==1:
                    break
                
                page += 1
            
            return all_results
            
        except requests.RequestException as e:
            raise DromAPIError(f"Network error: {str(e)}")
        except Exception as e:
            raise DromAPIError(f"Unexpected error: {str(e)}") 