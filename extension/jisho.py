import requests

url = "https://jisho.org/api/v1/search/words"

word = input("Enter a Japanese word: ")

params = {
    "keyword": word
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()["data"]
    if len(data) > 0:
        result = data[0]
        japanese = result["japanese"][0]["word"]
        english = result["senses"][0]["english_definitions"][0]
        reading = result["japanese"][0]["reading"]
        
        print(f"{japanese}: {english} {reading}")
    else:
        print("No results found.")
else:
    print("Error occurred while connecting to the API.")
