from googletrans import Translator

# Initialize translator object
translator = Translator()

# Define the Thai sentence to be translated
sentence_thai = "สวัสดีชาวโลก"

# Translate to Japanese
translation = translator.translate(sentence_thai, dest='ja').text

# Print the result
print(translation)
