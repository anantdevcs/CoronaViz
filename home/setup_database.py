from home.models import country_wise
import requests
def main():

    url = "https://api.covid19api.com/countries"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)

    return response



if __name__ == "__main__":
    main()

