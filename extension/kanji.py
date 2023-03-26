import requests


charater = "訪"
url = f"https://kanjialive-api.p.rapidapi.com/api/public/kanji/{charater}"

querystring = {"on":"シン"}

headers = {
	"X-RapidAPI-Key": "e7bc4869c5mshcc9bc8d01104e19p173e4ejsn129fe686cdbc",
	"X-RapidAPI-Host": "kanjialive-api.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
response = response.json()

onyomi = response["kanji"]["onyomi"]["katakana"]
kunyomi = response["kanji"]["kunyomi"]["hiragana"]
poster = response["kanji"]["video"]["poster"]
webm = response["kanji"]["video"]["webm"]
meaning = response["kanji"]["meaning"]["english"]

print(charater,onyomi,kunyomi,meaning)