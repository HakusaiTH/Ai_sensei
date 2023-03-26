import MeCab
import re

def cut_kanji(text):
    # Extract all Kanji characters using a regular expression
    kanji = re.findall(r'[一-龯]', text)
    
    return kanji

def cut_japanese_text(text):
    # Initialize MeCab
    m = MeCab.Tagger()
    
    # Parse the text with MeCab
    parsed_text = m.parse(text)
    
    # Split the parsed text into separate lines
    lines = parsed_text.split('\n')
    
    # Extract the first element from each line (the word or token)
    words = [line.split('\t')[0] for line in lines[:-2]]
    
    # Remove any words that do not contain any Kanji characters
    words = [word for word in words if re.search(r'[一-龯]', word)]
    
    return words

# Example usage
text = '私は日本語を勉強しています。'
kanji = cut_kanji(text)
japanese_text_words = cut_japanese_text(text)

print('Kanji:', kanji)
print('Japanese text words:', japanese_text_words)
