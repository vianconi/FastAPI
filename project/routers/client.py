import requests, os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

URL = "http://localhost:8000/api/v1/users/"

USER = {"username": user, "password": password}

response = requests.post(URL + "login", json=USER)

if response.status_code == 200:
    print("Usuario autenticado")

    # print(response.json(), response.cookies, response.cookies.get_dict())

    user_id = response.cookies.get_dict().get("user_id")

    cookies = {"user_id": user_id}

    response = requests.get(URL + "reviews", cookies=cookies)

    if response.status_code == 200:
        for review in response.json():
            print(f"> {review['review']} - {review['score']}")

else:
    print("error")
