import requests
from time import sleep
from fake_useragent import UserAgent

session = requests.Session()
ua = UserAgent()
headers = {
    "User-Agent": ua.chrome,
    "Accept": "application/json, */*",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.encar.com/",
    "Origin": "https://www.encar.com",
    "X-Requested-With": "XMLHttpRequest",
}

print("🔄 Получаю куки с encar.com...")
main_page_url = "https://www.encar.com"
response = session.get(main_page_url, headers=headers)

if response.status_code != 200:
    print(f"❌ Ошибка: {response.status_code}")
    exit()

print("✅ Куки получены:", session.cookies.get_dict())

sleep(2)

api_url = "http://api.encar.com/search/car/list/general?count=false&q=(And.Hidden.N._.CarType.A.)&inav=%7CMetadata%7CSort"
print("🔄 Делаю запрос к API...")

api_response = session.get(api_url, headers=headers)

if api_response.status_code == 200:
    print("✅ Успешно! Данные:")
    print(api_response.json())
else:
    print(f"❌ Ошибка API: {api_response.status_code}")
    print("Ответ сервера:", api_response.text)