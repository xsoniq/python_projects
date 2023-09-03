import requests
from config import API_TOKEN

params = {"q": "London", "appid": API_TOKEN}


def main():
    response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)

    # print(response.status_code)
    # print(response.headers)
    print(response.json())


if __name__ == "__main__":
    main()







