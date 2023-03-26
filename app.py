import openai
import MeCab
from googletrans import Translator
import re
import requests
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

openai.api_key = 'openai-key'

def cut_kanji(text):
    kanji = re.findall(r'[一-龯]', text)
    return kanji

def cut_japanese_text(text):
    m = MeCab.Tagger()
    parsed_text = m.parse(text)
    lines = parsed_text.split('\n')
    words = [line.split('\t')[0] for line in lines[:-2]]
    words = [word for word in words if re.search(r'[一-龯]', word)]
    return words

def genarate_examp(prompt) :    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    response_text = response.choices[0].text
    return response_text

def tran(para,lg) :
    translator = Translator()
    translation = translator.translate(para, dest=lg).text
    return translation

def jisho(word) :
    url = "https://jisho.org/api/v1/search/words"
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
            return f"({reading})  {english}"
        else:
            print("No results found.")
    else:
        print("Error occurred while connecting to the API.")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def genarate():
    user_input = request.form['data']    
    translation = tran(user_input,'ja')

    prompt = genarate_examp(f'Teach Japanese from this sentence [{translation}]')
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    response_text = response.choices[0].text
    response_text = tran(response_text,'th')

    url = "https://api.aiforthai.in.th/ssense"    
    params = {'text':response_text}
    headers = {'Apikey': "api.aiforthai"}
    response = requests.get(url, headers=headers, params=params).json()
    polarity_score = response['sentiment']['polarity']

    if polarity_score == '':
        polarity_score = 'neutral'

    kanji = cut_kanji(translation)
    japanese_text_words = cut_japanese_text(translation)

    #print(response_text,kanji,japanese_text_words)
    return jsonify({'ai':response_text,'sen':polarity_score,'response': translation, 'kanji': kanji,'word':japanese_text_words})

#kanji
@app.route('/dec_kanji', methods=['POST'])
def dec_kanji():
    charater = request.form['data']
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
    meaning = response["kanji"]["meaning"]["english"]

    example = genarate_examp(f'Describe this Kanji [{charater}]')
    result = onyomi,kunyomi
    image_url = response["kanji"]["video"]["poster"]

    translation_charater =  tran(charater,'th')
    return jsonify({'charater':charater,'translation_charater':meaning,'on':onyomi,'kun':kunyomi,'example':example,'image_url': image_url})

#word
@app.route('/dec_word', methods=['POST'])
def dec_word():
    word = request.form['data']

    #translation = tran(word,'th')
    translation = jisho(word) 

    example =  genarate_examp(f'Make a Japanese sentence from [{word}]')
    translation_example = tran(example,'th')

    return jsonify({'word':word,'result':translation,'translation_example':translation_example,'example':example})

if __name__ == '__main__':
    app.run(debug=True)
