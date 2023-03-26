import requests
 
url = "https://api.aiforthai.in.th/ssense"
 
text = f'"形態素解析器" ชอบมาก\n'
 
params = {'text':text}
 
headers = {
    'Apikey': "If66yNxYjCF1T5XtBgQ3k9VczUbHJn51"
}
 
response = requests.get(url, headers=headers, params=params).json()
polarity_score = response['sentiment']['polarity']

if polarity_score == '':
    polarity_score = 'neutral'

print(polarity_score)


